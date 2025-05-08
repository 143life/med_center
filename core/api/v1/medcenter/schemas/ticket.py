from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from core.api.v1.medcenter.schemas.person import PersonSchema
from core.api.v1.medcenter.schemas.request import TicketCreateRequest
from core.apps.medcenter.entities.ticket import Ticket as TicketEntity


class TicketSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = Field(default=None, exclude=True)  # noqa
    person: "PersonSchema"
    datetime: datetime
    number: int
    completed: bool

    @staticmethod
    def from_entity(entity: TicketEntity) -> "TicketSchema":
        return TicketSchema(
            id=entity.id,
            person=PersonSchema.from_entity(entity.person),
            datetime=entity.datetime,
            number=entity.number,
            completed=entity.completed,
        )

    @staticmethod
    def to_entity(schema: "TicketSchema") -> TicketEntity:
        return TicketEntity(
            id=schema.id,
            person=PersonSchema.to_entity(schema.person),
            datetime=schema.datetime,
            number=schema.number,
            completed=schema.completed,
        )

    @staticmethod
    def from_ticket_create_request(
        schema: TicketCreateRequest,
    ) -> "TicketSchema":
        return TicketSchema(
            person=schema.person,
            datetime=schema.datetime,
            number=schema.number,
            completed=schema.completed,
        )
