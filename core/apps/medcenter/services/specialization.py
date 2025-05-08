from collections.abc import Iterable

from django.db.models import Q

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

    @classmethod
    def get_specialization_list(cls) -> Iterable[Specialization]:
        qs = cls.model.objects.all()

        return [dto.to_entity() for dto in qs]
