from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.api.v1.medcenter.filters import DoctorFilters
from core.apps.medcenter.entities.doctor import Doctor
from core.apps.medcenter.models import Doctor as DoctorDTO


class BaseDoctorService(ABC):

    @abstractmethod
    def get_doctor_list(
        self,
        filters: DoctorFilters,
        pagination: PaginationIn,
    ) -> Iterable[Doctor]: ...

    @abstractmethod
    def get_doctor_count(self, filters: DoctorFilters) -> int: ...


class ORMDoctorService(BaseDoctorService):
    def _build_doctor_query(self, filters: DoctorFilters) -> Q:
        query = Q()

        return query

    def get_doctor_list(
        self,
        filters: DoctorFilters,
        pagination: PaginationIn,
    ) -> Iterable[Doctor]:
        query = self._build_doctor_query(filters)
        qs = DoctorDTO.objects.filter(query)[
            pagination.offset : pagination.offset + pagination.limit  # noqa
        ]

        return [doctor.to_entity() for doctor in qs]

    def get_doctor_count(self, filters: DoctorFilters) -> int:
        query = self._build_doctor_query(filters)

        return DoctorDTO.objects.filter(query).count()
