from ninja import Schema


class PersonFilters(Schema):
    search: str | None = None


class DoctorScheduleFilters(Schema):
    search: str | None = None


class DoctorFilters(Schema):
    search: str | None = None


class SpecializationFilters(Schema):
    search: str | None = None


class TicketFilters(Schema):
    search: str | None = None


class AppointmentFilters(Schema):
    search: str | None = None
    ticket: int | None = None


class ScheduleFilters(Schema):
    search: str | None = None


class WaitingListFilters(Schema):
    search: str | None = None
