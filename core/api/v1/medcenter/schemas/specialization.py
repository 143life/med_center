from pydantic import BaseModel

from core.apps.medcenter.entities.specialization import (
    Specialization as SpecializationEntity,
)


class SpecializationSchema(BaseModel):
    title: str

    @staticmethod
    def from_entity(entity: SpecializationEntity) -> "SpecializationSchema":
        return SpecializationSchema(title=entity.title)
