from django.contrib import admin

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


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("person", "datetime", "number", "completed")


@admin.register(WaitingList)
class WaitingListAdmin(admin.ModelAdmin):
    list_display = ("ticket", "time_begin", "time_end")
