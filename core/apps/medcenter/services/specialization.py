from collections.abc import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.api.v1.medcenter.filters import SpecializationFilters
from core.apps.medcenter.entities import Specialization
from core.apps.medcenter.models import Specialization as SpecializationDTO
from core.apps.medcenter.services.base import BaseService


class ORMSpecializationService(
    BaseService[SpecializationFilters, Specialization, SpecializationDTO],
):
    filters = SpecializationFilters
    entity = Specialization
    model = SpecializationDTO

    @classmethod
    def _build_query(cls, filters: SpecializationFilters) -> Q:
        query = Q()

        return query

    def get_specialization_list(
        self,
        filters: SpecializationFilters,
        pagination: PaginationIn,
    ) -> Iterable[Specialization]:
        return ORMSpecializationService.get_list(
            filters=filters,
            pagination=pagination,
        )

    def get_specialization_count(self, filters: SpecializationFilters) -> int:
        return ORMSpecializationService.get_count(filters=filters)
