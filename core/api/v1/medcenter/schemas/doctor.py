from pydantic import (
    BaseModel,
    ConfigDict,
)

from core.api.v1.medcenter.schemas.person import PersonSchema
from core.api.v1.medcenter.schemas.specialization import SpecializationSchema
from core.apps.medcenter.entities.doctor import Doctor as DoctorEntity


class DoctorSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    person: "PersonSchema"
    specialization: "SpecializationSchema"

    @staticmethod
    def from_entity(entity: DoctorEntity) -> "DoctorSchema":
        return DoctorSchema(
            person=PersonSchema.from_entity(entity.person),
            specialization=SpecializationSchema.from_entity(
                entity.specialization,
            ),
        )
