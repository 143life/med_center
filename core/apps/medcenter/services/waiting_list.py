from collections.abc import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.api.v1.medcenter.filters import WaitingListFilters
from core.apps.medcenter.entities import WaitingList
from core.apps.medcenter.models import WaitingList as WaitingListDTO
from core.apps.medcenter.services.base import BaseService


class ORMWaitingListService(BaseService[WaitingListFilters, WaitingList, WaitingListDTO]):
	filters = WaitingListFilters
	entity = WaitingList
	model = WaitingListDTO

	@classmethod
	def _build_query(cls, filters: WaitingListFilters) -> Q:
		query = Q()
		
		return query

	def get_waiting_list_list(
		self,
		filters: WaitingListFilters,
		pagination: PaginationIn,
	) -> Iterable[WaitingList]:
		return ORMWaitingListService.get_list(
			filters=filters,
			pagination=pagination
		)

	def get_waiting_list_count(self, filters: WaitingListFilters) -> int:
		return ORMWaitingListService.get_count(
			filters=filters
		)