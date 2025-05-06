from pydantic import BaseModel

from core.apps.medcenter.entities.specialization import (
    Specialization as SpecializationEntity,
)


class SpecializationSchema(BaseModel):
    title: str

    @staticmethod
    def from_entity(entity: SpecializationEntity) -> "SpecializationSchema":
        return SpecializationSchema(title=entity.title)

    @staticmethod
    def to_entity(schema: "SpecializationSchema") -> SpecializationEntity:
        return SpecializationEntity(title=schema.title)
