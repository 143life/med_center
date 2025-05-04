from dataclasses import dataclass

from core.apps.medcenter.entities.doctor import Doctor
from core.apps.medcenter.entities.schedule import Schedule

@dataclass
class DoctorSchedule:
	doctor: "Doctor"
	schedule: "Schedule"
	cabinet_number: int