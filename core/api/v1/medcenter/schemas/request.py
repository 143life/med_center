from datetime import datetime

from ninja import Schema


class TicketCreateRequest(Schema):
    id: int  # noqa
    first_name: str
    last_name: str
    patronymic: str
    date_birth: datetime | None = None
    datetime: datetime
    number: int
    completed: bool
    appointment_list: list[dict]
