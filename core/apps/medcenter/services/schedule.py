from django.db.models import Q

from core.api.v1.medcenter.filters import ScheduleFilters
from core.apps.medcenter.entities import Schedule
from core.apps.medcenter.models import Schedule as ScheduleDTO
from core.apps.medcenter.services.base import BaseService


class ORMScheduleService(BaseService[ScheduleFilters, Schedule, ScheduleDTO]):
    filters = ScheduleFilters
    entity = Schedule
    model = ScheduleDTO

    @classmethod
    def _build_query(cls, filters: ScheduleFilters) -> Q:
        query = Q()

        return query
