from ninja import Schema


class PersonFilters(Schema):
    search: str | None = None
