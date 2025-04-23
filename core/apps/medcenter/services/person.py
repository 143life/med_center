from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.api.v1.medcenter.filters import PersonFilters
from core.apps.medcenter.entities.person import Person
from core.apps.medcenter.models.person import Person as PersonDTO


class BasePersonService(ABC):
    """Abstract class for business logic"""

    @abstractmethod
    def get_person_list(
        self,
        filters: PersonFilters,
        pagination: PaginationIn,
    ) -> Iterable[Person]: ...
    @abstractmethod
    def get_person_count(self, filters: PersonFilters) -> int: ...


# TODO: закинуть фильтры в сервисный слой, чтобы избежать нарушения D из SOLID
class ORMPersonService(BasePersonService):
    def _build_product_query(self, filters: PersonFilters) -> Q:
        query = Q()  # is_visible=True

        if filters.search is not None:
            query &= (
                Q(first_name__icontains=filters.search)
                | Q(last_name__icontains=filters.search)
                | Q(patronymic__icontains=filters.search)
                | Q(date_birth__icontains=filters.search)
            )
        return query

    def get_person_list(
        self,
        filters: PersonFilters,
        pagination: PaginationIn,
    ) -> Iterable[Person]:
        query = self._build_product_query(filters)
        qs = PersonDTO.objects.filter(query)[
            pagination.offset : pagination.offset + pagination.limit  # noqa
        ]  # maybe is_visible=True later

        return [person.to_entity() for person in qs]

    def get_person_count(self, filters: PersonFilters) -> int:
        query = self._build_product_query(filters)

        return PersonDTO.objects.filter(
            query,
        ).count()  # maybe is_visible=True later (in filter)
