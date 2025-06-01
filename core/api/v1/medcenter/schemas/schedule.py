from datetime import datetime

from pydantic import BaseModel

from core.apps.medcenter.entities.schedule import Schedule as ScheduleEntity


class ScheduleSchema(BaseModel):
    id: int  # noqa
    datetime_begin: datetime
    datetime_end: datetime
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    sunday: bool

    @staticmethod
    def from_entity(entity: ScheduleEntity) -> "ScheduleSchema":
        return ScheduleSchema(
            id=entity.id,
            datetime_begin=entity.datetime_begin,
            datetime_end=entity.datetime_end,
            monday=entity.monday,
            tuesday=entity.tuesday,
            wednesday=entity.wednesday,
            thursday=entity.thursday,
            friday=entity.friday,
            saturday=entity.saturday,
            sunday=entity.sunday,
        )
