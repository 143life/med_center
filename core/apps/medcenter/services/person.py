from django.db.models import Q

from core.api.v1.medcenter.filters import PersonFilters
from core.apps.medcenter.entities.person import Person
from core.apps.medcenter.models.person import Person as PersonDTO
from core.apps.medcenter.services.base import BaseService


# TODO: закинуть фильтры в сервисный слой, чтобы избежать нарушения D из SOLID
class ORMPersonService(BaseService[PersonFilters, Person, PersonDTO]):
    filters = PersonFilters
    entity = Person
    model = PersonDTO

    @classmethod
    def _build_query(cls, filters: PersonFilters) -> Q:
        query = Q()  # is_visible=True

        if filters.search is not None:
            query &= (
                Q(first_name__icontains=filters.search)
                | Q(last_name__icontains=filters.search)
                | Q(patronymic__icontains=filters.search)
                | Q(date_birth__icontains=filters.search)
            )
        return query
