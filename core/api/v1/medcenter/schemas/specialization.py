from pydantic import BaseModel

from core.apps.medcenter.entities.specialization import (
    Specialization as SpecializationEntity,
)


class SpecializationSchema(BaseModel):
    id: int  # noqa
    title: str

    @staticmethod
    def from_entity(entity: SpecializationEntity) -> "SpecializationSchema":
        return SpecializationSchema(id=entity.id, title=entity.title)

    @staticmethod
    def to_entity(schema: "SpecializationSchema") -> SpecializationEntity:
        return SpecializationEntity(id=schema.id, title=schema.title)
