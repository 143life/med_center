from pydantic import BaseModel, ConfigDict

from core.api.v1.medcenter.schemas.doctor import DoctorSchema
from core.api.v1.medcenter.schemas.schedule import ScheduleSchema
from core.apps.medcenter.entities.doctor_schedule import DoctorSchedule as DoctorScheduleEntity

class DoctorScheduleSchema(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	doctor: "DoctorSchema"
	schedule: "ScheduleSchema"
	cabinet_number: int

	@staticmethod
	def from_entity(entity: DoctorScheduleEntity) -> "DoctorScheduleSchema":
		return DoctorScheduleSchema(
			doctor=DoctorSchema.from_entity(entity.doctor),
			schedule=ScheduleSchema.from_entity(entity.schedule),
			cabinet_number=entity.cabinet_number
		)