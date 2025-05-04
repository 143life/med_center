from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
)

from core.api.v1.medcenter.schemas.doctor_schedule import DoctorScheduleSchema
from core.api.v1.medcenter.schemas.ticket import TicketSchema
from core.apps.medcenter.entities import WaitingList as WaitingListEntity


class WaitingListSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ticket: "TicketSchema"
    doctor_schedule: "DoctorScheduleSchema"
    time_begin: datetime
    time_end: datetime

    @staticmethod
    def from_entity(entity: WaitingListEntity) -> "WaitingListSchema":
        return WaitingListSchema(
            ticket=TicketSchema.from_entity(entity.ticket),
            doctor_schedule=DoctorScheduleSchema.from_entity(
                entity.doctor_schedule,
            ),
            time_begin=entity.time_begin,
            time_end=entity.time_end,
        )
