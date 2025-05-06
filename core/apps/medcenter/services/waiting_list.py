from django.db.models import Q

from core.api.v1.medcenter.filters import WaitingListFilters
from core.apps.medcenter.entities import WaitingList
from core.apps.medcenter.models import WaitingList as WaitingListDTO
from core.apps.medcenter.services.base import BaseService


class ORMWaitingListService(
    BaseService[WaitingListFilters, WaitingList, WaitingListDTO],
):
    filters = WaitingListFilters
    entity = WaitingList
    model = WaitingListDTO

    @classmethod
    def _build_query(cls, filters: WaitingListFilters) -> Q:
        query = Q()

        return query
