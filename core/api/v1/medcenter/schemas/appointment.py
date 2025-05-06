from pydantic import (
    BaseModel,
    ConfigDict,
)

from core.api.v1.medcenter.schemas.response import AppointmentOut
from core.api.v1.medcenter.schemas.specialization import SpecializationSchema
from core.api.v1.medcenter.schemas.ticket import TicketSchema
from core.apps.medcenter.entities.appointment import (
    Appointment as AppointmentEntity,
)


class AppointmentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ticket: "TicketSchema"
    specialization: "SpecializationSchema"
    completed: bool

    @staticmethod
    def from_entity(entity: AppointmentEntity) -> "AppointmentSchema":
        return AppointmentSchema(
            ticket=TicketSchema.from_entity(entity.ticket),
            specialization=SpecializationSchema.from_entity(
                entity.specialization,
            ),
            completed=entity.completed,
        )

    @staticmethod
    def to_entity(schema: "AppointmentSchema") -> AppointmentEntity:
        return AppointmentEntity(
            ticket=TicketSchema.to_entity(schema.ticket),
            specialization=SpecializationSchema.to_entity(
                schema.specialization,
            ),
            completed=schema.completed,
        )

    def to_appointment_out(self) -> "AppointmentOut":
        return AppointmentOut(
            specialization=self.specialization.title,
            completed=self.completed,
        )
