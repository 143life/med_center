from dataclasses import dataclass
from datetime import datetime

from core.apps.medcenter.entities.doctor_schedule import DoctorSchedule
from core.apps.medcenter.entities.ticket import Ticket


@dataclass
class WaitingList:
    ticket: "Ticket"
    doctor_schedule: "DoctorSchedule"
    time_begin: datetime
    time_end: datetime