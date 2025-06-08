from datetime import timedelta

from django.db import transaction
from django.db.models import (
    Count,
    Q,
)
from django.utils import timezone

from core.apps.medcenter.models.appointment import Appointment
from core.apps.medcenter.models.doctor_schedule import DoctorSchedule
from core.apps.medcenter.models.ticket import Ticket
from core.apps.medcenter.models.waiting_list import WaitingList
from core.celery import app


@app.task(bind=True)
def auto_complete_appointments_and_delete_from_waiting_list(
    self,
    *args,
    **kwargs,
):
    with transaction.atomic():
        # 1. Находим просроченные записи в очереди с незавершенными талонами
        expired_waiting = WaitingList.objects.filter(
            time_end__lte=timezone.now(),
            ticket__completed=False,  # Проверяем статус в Ticket
        ).select_related("ticket", "doctor_schedule__doctor__specialization")

        if not expired_waiting.exists():
            return {"updated_appointments": 0, "deleted_waitings": 0}

        # 2. Получаем ID талонов для массового обновления
        ticket_ids = expired_waiting.values_list("ticket_id", flat=True)
        specialization_ids = expired_waiting.values_list(
            "doctor_schedule__doctor__specialization_id",
            flat=True,
        ).distinct()

        # 3. Обновляем связанные Appointment
        updated_appointments = Appointment.objects.filter(
            ticket_id__in=ticket_ids,
            specialization_id__in=specialization_ids,
            completed=False,
        ).update(completed=True)

        # 4. Удаляем все завершенные приемы из очереди
        deleted_waitings, _ = WaitingList.objects.filter(
            ticket_id__in=ticket_ids,
        ).delete()

        return {
            "updated_appointments": updated_appointments,
            "deleted_waitings": deleted_waitings,
        }


@app.task(bind=True)
def auto_update_to_waiting_list(self, *args, **kwargs):
    with transaction.atomic():
        now = timezone.now()
        current_weekday = now.strftime("%A").lower()

        # 1. Проверяем размер очереди
        current_queue = WaitingList.objects.filter(time_end__gt=now)
        if current_queue.count() >= 20:
            return

        # 2. Находим незавершенные приемы, не в очереди
        busy_ticket_ids = current_queue.values_list("ticket_id", flat=True)
        uncompleted_appointments = (
            Appointment.objects.filter(completed=False)
            .exclude(ticket_id__in=busy_ticket_ids)
            .select_related("specialization", "ticket")
            .order_by("ticket__created_at")
        )

        # 3. Получаем ID специализаций из незавершенных приемов
        specialization_ids = uncompleted_appointments.values_list(
            "specialization_id",
            flat=True,
        ).distinct()

        # 4. Ищем работающих врачей нужных специализаций
        working_doctors = (
            DoctorSchedule.objects.filter(
                schedule__datetime_begin__lte=now,
                schedule__datetime_end__gt=now,
                **{f"schedule__{current_weekday}": True},
                doctor__specialization_id__in=specialization_ids,
            )
            .annotate(
                appointment_count=Count(
                    "waitinglist",
                    filter=Q(waitinglist__time_end__gt=now),
                ),
            )
            .select_related("doctor", "doctor__specialization", "schedule")
            .order_by("appointment_count", "doctor_id")
        )

        if not working_doctors.exists():
            return

        # 6. Обрабатываем записи
        for doctor in working_doctors:
            last_appointment = (
                current_queue.filter(doctor_schedule=doctor)
                .order_by("-time_end")
                .first()
            )

            for appointment in uncompleted_appointments:
                if (
                    appointment.specialization_id
                    == doctor.doctor.specialization_id
                ):
                    if doctor.appointment_count == 0:
                        # Свободный врач - добавляем сразу
                        WaitingList.objects.create(
                            ticket=appointment.ticket,
                            doctor_schedule=doctor,
                            time_begin=now,
                            time_end=now + timedelta(minutes=11),
                        )
                        return
                    # в противном случае подбираем время для добавления
                    new_start = (
                        last_appointment.time_end if last_appointment else now
                    )
                    new_start = max(new_start, now)

                    work_end = doctor.schedule.datetime_end
                    if (work_end - new_start) >= timedelta(minutes=11):
                        WaitingList.objects.create(
                            ticket=appointment.ticket,
                            doctor_schedule=doctor,
                            time_begin=new_start,
                            time_end=new_start + timedelta(minutes=11),
                        )
                        return
        return


@app.task(bind=True)
def auto_complete_tickets(self, *args, **kwargs):
    """
    Помечает талоны как завершенные,
    если все связанные с ними приемы завершены.
    """
    with transaction.atomic():
        # Находим все незавершенные талоны
        uncompleted_tickets = Ticket.objects.filter(completed=False)

        # Для каждого талона проверяем, все ли его приемы завершены
        tickets_to_complete = []
        for ticket in uncompleted_tickets:
            # Проверяем, есть ли незавершенные приемы
            has_uncompleted = Appointment.objects.filter(
                ticket=ticket,
                completed=False,
            ).exists()

            # Если все приемы завершены, добавить талон в список
            if not has_uncompleted:
                tickets_to_complete.append(ticket.id)

        # Обновляем статус талонов
        if tickets_to_complete:
            updated_count = Ticket.objects.filter(
                id__in=tickets_to_complete,
            ).update(completed=True)
        else:
            updated_count = 0

        return {
            "updated_tickets": updated_count,
            "ticket_ids": tickets_to_complete,
        }
