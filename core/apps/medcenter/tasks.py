from collections import defaultdict
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from core.apps.medcenter.models.appointment import Appointment
from core.apps.medcenter.models.doctor_schedule import DoctorSchedule
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

        # TODO: обновлять заодно и талоны, если все приемы завершены

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
        current_queue = WaitingList.objects.filter(
            time_end__gt=now,
        ).select_related("doctor_schedule__doctor__specialization")

        if current_queue.count() >= 10:
            return

        # 2. Находим незавершенные приемы не в очереди
        busy_ticket_ids = current_queue.values_list("ticket_id", flat=True)
        uncompleted_appointments = (
            Appointment.objects.filter(completed=False)
            .exclude(ticket_id__in=busy_ticket_ids)
            .select_related("specialization")
        )

        if not uncompleted_appointments.exists():
            return

        # 3. Ищем работающих сегодня врачей
        working_doctors = DoctorSchedule.objects.filter(
            schedule__datetime_begin__lte=now,
            schedule__datetime_end__gt=now,
            **{f"schedule__{current_weekday}": True},
        ).select_related("doctor__specialization")

        if not working_doctors.exists():
            return

        # 4. Ищем свободных врачей прямо сейчас
        busy_doctor_ids = current_queue.filter(
            doctor_schedule__in=working_doctors,
        ).values_list("doctor_schedule_id", flat=True)

        free_doctors = working_doctors.exclude(id__in=busy_doctor_ids)

        if free_doctors.exists():
            assign_to_available_doctor(
                uncompleted_appointments,
                free_doctors,
                now,
            )
            return

        # 5. Пытаемся запланировать на ближайшее освобождающееся время
        ending_appointments = current_queue.order_by("time_end")

        for ending_appt in ending_appointments:
            doctor = ending_appt.doctor_schedule.doctor
            end_time = ending_appt.time_end

            # Проверяем продолжение работы врача
            next_schedule = DoctorSchedule.objects.filter(
                doctor=doctor,
                schedule__datetime_begin__lte=end_time,
                schedule__datetime_end__gte=end_time + timedelta(minutes=30),
                **{f'schedule__{end_time.strftime("%A").lower()}': True},
            ).first()

            if not next_schedule:
                continue

            # Ищем подходящий незавершенный прием для этой специализации
            suitable_appointment = uncompleted_appointments.filter(
                specialization=doctor.specialization,
            ).first()

            if suitable_appointment:
                WaitingList.objects.create(
                    ticket=suitable_appointment.ticket,
                    doctor_schedule=next_schedule,
                    time_begin=end_time,
                    time_end=end_time + timedelta(minutes=10),
                )
                return  # Выходим после первого успешного назначения


def assign_to_available_doctor(appointments, doctors, now):
    """Назначает первый подходящий прием свободному врачу"""
    # Группируем врачей по специализациям
    spec_map = defaultdict(list)
    for doc in doctors:
        spec_map[doc.doctor.specialization_id].append(doc)

    # Ищем первый подходящий прием
    for appointment in appointments.order_by("ticket_id"):
        if appointment.specialization_id in spec_map:
            # Берем первого свободного врача нужной специализации
            doctor_schedule = spec_map[appointment.specialization_id][0]

            WaitingList.objects.create(
                ticket=appointment.ticket,
                doctor_schedule=doctor_schedule,
                time_begin=now,
                time_end=now + timedelta(minutes=10),
            )
            break
