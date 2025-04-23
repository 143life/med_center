from ninja import Schema


class PersonFilters(Schema):
    search: str | None = None


class DoctorFilters(Schema):
    search: str | None = None


class SpecializationFilters(Schema):
    search: str | None = None
