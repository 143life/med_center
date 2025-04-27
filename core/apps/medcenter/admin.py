from django.contrib import admin
from django.contrib.admin import AdminSite

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


class MyAdminSite(AdminSite):
    site_header = "Название сайта"  # Название вверху страницы админки
    site_title = "Админка сайта"  # Название вкладки браузера
    index_title = "Добро пожаловать!"  # Название на главной админке

    def each_context(self, request):
        context = super().each_context(request)
        context["site_title"] = self.site_title
        return context


class CustomAdmin(admin.ModelAdmin):
    class Media:
        css = {"all": ("admin/custom/custom.css",)}


# Создаем свой экземпляр админки
admin_site = MyAdminSite(name="myadmin")


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
    search_fields = ["first_name", "last_name", "patronymic", "date_birth"]
    list_filter = ["last_name"]


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
