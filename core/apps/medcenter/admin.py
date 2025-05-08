from django import forms
from django.conf import settings
from django.contrib import admin
from django.db import transaction

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
class AppointnmentAdmin(admin.ModelAdmin):
    list_display = ("ticket", "specialization")


@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ("cabinet_number", "doctor", "schedule")


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("person", "specialization")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("datetime_begin", "datetime_end")


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin): ...  # noqa


@admin.register(WaitingList)
class WaitingListAdmin(admin.ModelAdmin):
    list_display = ("ticket", "time_begin", "time_end")


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
        # Получаем доступные специальности через API
        # URL API из настроек
        api_url = f"{settings.API_BASE_URL}medcenter/specialization/all"

        try:
            response = requests.get(
                api_url,
                timeout=3,  # Таймаут 3 секунды
                headers={"Accept": "application/json"},
            )
            if response.status_code == 200:
                specialties = response.json().get("data", [])
                self.fields["available_specialities"].choices = [
                    (spec["id"], spec["title"]) for spec in specialties
                ]
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    form = TicketAdminForm
    list_display = ("person", "datetime", "number", "completed")

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
