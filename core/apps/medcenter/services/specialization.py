from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.api.v1.medcenter.filters import SpecializationFilters
from core.apps.medcenter.entities import Specialization
from core.apps.medcenter.models import Specialization as SpecializationDTO


class BaseSpecializationService(ABC):

    @abstractmethod
    def get_specialization_list(
        self,
        filters: SpecializationFilters,
        pagination: PaginationIn,
    ) -> Iterable[Specialization]: ...

    @abstractmethod
    def get_specialization_count(
        self,
        filters: SpecializationFilters,
    ) -> int: ...


class ORMSpecializationService(BaseSpecializationService):
    def _build_specialization_query(self, filters: SpecializationFilters) -> Q:
        query = Q()

        if filters.search is not None:
            query &= Q(title__icontains=filters.search)

        return query

    def get_specialization_list(
        self,
        filters: SpecializationFilters,
        pagination: PaginationIn,
    ) -> Iterable[Specialization]:
        query = self._build_specialization_query(filters)
        qs = SpecializationDTO.objects.filter(query)[
            pagination.offset : pagination.offset + pagination.limit  # noqa
        ]

        return [specialization.to_entity() for specialization in qs]

    def get_specialization_count(self, filters: SpecializationFilters) -> int:
        query = self._build_specialization_query(filters)

        return SpecializationDTO.objects.filter(query).count()
