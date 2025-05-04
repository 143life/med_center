from pydantic import BaseModel, ConfigDict

from core.api.v1.medcenter.schemas.specialization import SpecializationSchema
from core.api.v1.medcenter.schemas.ticket import TicketSchema
from core.apps.medcenter.entities.appointment import Appointment as AppointmentEntity

class AppointmentSchema(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	ticket: "TicketSchema"
	specialization: "SpecializationSchema"
	completed: bool

	@staticmethod
	def from_entity(entity: AppointmentEntity) -> "AppointmentSchema":
		return AppointmentSchema(
			ticket = TicketSchema.from_entity(entity.ticket),
			specialization = SpecializationSchema.from_entity(entity.specialization),
			completed = entity.completed
		)