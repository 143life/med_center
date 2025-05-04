from collections.abc import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.api.v1.medcenter.filters import TicketFilters
from core.apps.medcenter.entities import Ticket
from core.apps.medcenter.models import Ticket as TicketDTO
from core.apps.medcenter.services.base import BaseService


class ORMTicketService(BaseService[TicketFilters, Ticket, TicketDTO]):
    filters = TicketFilters
    entity = Ticket
    model = TicketDTO

    @classmethod
    def _build_query(cls, filters: TicketFilters) -> Q:
        query = Q()

        return query

    def get_ticket_list(
        self,
        filters: TicketFilters,
        pagination: PaginationIn,
    ) -> Iterable[Ticket]:
        return ORMTicketService.get_list(
            filters=filters,
            pagination=pagination,
        )

    def get_ticket_count(self, filters: TicketFilters) -> int:
        return ORMTicketService.get_count(filters=filters)
