from django.contrib import admin
from .models import Appointment, DoctorSchedule, Doctor, Person, Schedule, Specialization, Ticket, WaitingList

# Register your models here.
admin.site.register(Appointment)
admin.site.register(DoctorSchedule)
admin.site.register(Doctor)
admin.site.register(Person)
admin.site.register(Schedule)
admin.site.register(Specialization)
admin.site.register(Ticket)
admin.site.register(WaitingList)