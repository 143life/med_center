from django import forms
from django.conf import settings
from django.contrib import admin
from django.db import transaction
from django.urls import reverse
from django.utils.html import format_html

import requests

from core.api.v1.medcenter.handlers.ticket import TicketHandler
from core.api.v1.medcenter.schemas.person import PersonSchema
from core.api.v1.medcenter.schemas.request import TicketCreateRequest

from .models import (
    Appointment,
    Doctor,
    DoctorSchedule,
    Person,
    Schedule,
    Specialization,
    Ticket,
    WaitingList,
)


# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("ticket", "specialization", "completed")
    list_filter = ("completed", "specialization")
    search_fields = ("ticket__number", "specialization__title")
    raw_id_fields = ("ticket", "specialization")


@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ("doctor", "schedule", "cabinet_number")
    list_filter = (
        "cabinet_number",
        "schedule__datetime_begin",
        "schedule__datetime_end",
    )
    search_fields = ("doctor__person__last_name", "doctor__person__first_name")
    raw_id_fields = ("doctor", "schedule")


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("person", "specialization")
    list_filter = ("specialization",)
    search_fields = (
        "person__last_name",
        "person__first_name",
        "person__patronymic",
    )
    raw_id_fields = ("person",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "patronymic", "date_birth")
    list_filter = ("date_birth",)
    search_fields = ("last_name", "first_name", "patronymic")
    ordering = ("last_name", "first_name")


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("datetime_begin", "datetime_end", "get_weekdays")
    list_filter = (
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    )
    date_hierarchy = "datetime_begin"

    def get_weekdays(self, obj):
        days = []
        if obj.monday:
            days.append("Пн")
        if obj.tuesday:
            days.append("Вт")
        if obj.wednesday:
            days.append("Ср")
        if obj.thursday:
            days.append("Чт")
        if obj.friday:
            days.append("Пт")
        if obj.saturday:
            days.append("Сб")
        if obj.sunday:
            days.append("Вс")
        return ", ".join(days)

    get_weekdays.short_description = "Дни недели"


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(WaitingList)
class WaitingListAdmin(admin.ModelAdmin):
    list_display = ("ticket", "doctor_schedule", "time_begin", "time_end")
    list_filter = ("time_begin", "time_end")
    search_fields = (
        "ticket__number",
        "doctor_schedule__doctor__person__last_name",
    )
    date_hierarchy = "time_begin"
    raw_id_fields = ("ticket", "doctor_schedule")


class TicketAdminForm(forms.ModelForm):
    available_specialities = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[],  # Будем заполнять динамически
        label="Доступные специальности",
    )

    class Meta:
        model = Ticket
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")

        # Заполняем специальности, только если это новый талон
        if not (instance and instance.pk):
            # Получаем доступные специальности через API
            api_url = f"{settings.API_BASE_URL}medcenter/specialization/all"

            try:
                response = requests.get(
                    api_url,
                    timeout=3,  # Таймаут 3 секунды
                    headers={"Accept": "application/json"},
                )
                if response.status_code == 200:
                    specialties = response.json().get("data", [])
                    if "available_specialities" in self.fields:
                        self.fields["available_specialities"].choices = [
                            (spec["id"], spec["title"]) for spec in specialties
                        ]
            except requests.exceptions.RequestException as e:
                print(f"API request failed: {e}")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    form = TicketAdminForm
    list_display = ("number", "person", "datetime", "completed")
    list_filter = ("completed", "datetime")
    search_fields = ("number", "person__last_name", "person__first_name")
    date_hierarchy = "datetime"
    raw_id_fields = ("person",)
    readonly_fields = ("ticket_progress_link",)

    def ticket_progress_link(self, obj):
        if obj.pk:
            url = reverse("medcenter:ticket_progress", args=[obj.pk])
            return format_html(
                '<a href="{}" class="button">Отследить процесс</a>',
                url,
            )
        return "Сохраните талон, чтобы отследить процесс"

    ticket_progress_link.short_description = "Процесс"

    def get_fieldsets(self, request, obj=None):
        if obj:  # Страница редактирования существующего талона
            return (
                ("Отслеживание", {"fields": ("ticket_progress_link",)}),
                (
                    "Основная информация",
                    {"fields": ("person", "datetime", "number", "completed")},
                ),
            )
        # Страница создания нового талона
        return (
            (
                "Основная информация",
                {"fields": ("person", "datetime", "number", "completed")},
            ),
            ("Назначить приёмы", {"fields": ("available_specialities",)}),
        )

    def save_model(self, request, obj, form, change):
        with transaction.atomic():
            # only if create ticket
            if not change:

                # Получаем полные данные о специальностях
                selected_specialities = form.cleaned_data.get(
                    "available_specialities",
                    [],
                )

                payload = TicketCreateRequest(
                    person=PersonSchema(
                        id=obj.person.id,
                        first_name=obj.person.first_name,
                        last_name=obj.person.last_name,
                        patronymic=obj.person.patronymic,
                        date_birth=obj.person.date_birth,
                    ),
                    datetime=obj.datetime,
                    number=obj.number,
                    completed=obj.completed,
                    appointment_list=selected_specialities,
                )

                # TODO: use requests, not service
                TicketHandler.create_ticket_handler(
                    request,
                    payload,
                )
            else:
                super().save_model(request, obj, form, change)
