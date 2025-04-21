from datetime import datetime
from pydantic import BaseModel

from core.apps.medcenter.entities.person import Person as PersonEntity


class PersonSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: str
    date_birth: datetime | None = None

    @staticmethod
    def from_entity(entity: PersonEntity) -> "PersonSchema":
        return PersonSchema(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            patronymic=entity.patronymic,
            date_birth=entity.date_birth,
        )


PersonListSchema = list[PersonSchema]
