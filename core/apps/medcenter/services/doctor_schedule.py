from django.db.models import Q

from core.api.v1.medcenter.filters import DoctorScheduleFilters
from core.apps.medcenter.entities import DoctorSchedule
from core.apps.medcenter.models import DoctorSchedule as DoctorScheduleDTO
from core.apps.medcenter.services.base import BaseService


class ORMDoctorScheduleService(
    BaseService[DoctorScheduleFilters, DoctorSchedule, DoctorScheduleDTO],
):
    filters = DoctorScheduleFilters
    entity = DoctorSchedule
    model = DoctorScheduleDTO

    @classmethod
    def _build_query(cls, filters: DoctorScheduleFilters) -> Q:
        query = Q()

        return query
