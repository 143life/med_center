from datetime import datetime

from ninja import Schema

from core.api.v1.medcenter.schemas.person import PersonSchema


class TicketCreateRequest(Schema):
    person: "PersonSchema"
    datetime: datetime
    number: int
    completed: bool
    appointment_list: list[int]
