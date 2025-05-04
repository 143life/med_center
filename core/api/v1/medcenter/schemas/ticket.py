from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
)

from core.api.v1.medcenter.schemas.person import PersonSchema
from core.apps.medcenter.entities.ticket import Ticket as TicketEntity


class TicketSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    person: "PersonSchema"
    datetime: datetime
    number: int
    completed: bool

    @staticmethod
    def from_entity(entity: TicketEntity) -> "TicketSchema":
        return TicketSchema(
            person=PersonSchema.from_entity(entity.person),
            datetime=entity.datetime,
            number=entity.number,
            completed=entity.completed,
        )
