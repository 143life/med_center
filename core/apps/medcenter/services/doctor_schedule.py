from collections.abc import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
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

    def get_doctor_schedule_list(
        self,
        filters: DoctorScheduleFilters,
        pagination: PaginationIn,
    ) -> Iterable[DoctorSchedule]:
        return ORMDoctorScheduleService.get_list(
            filters=filters,
            pagination=pagination,
        )

    def get_doctor_schedule_count(self, filters: DoctorScheduleFilters) -> int:
        return ORMDoctorScheduleService.get_count(filters=filters)
