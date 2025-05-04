from collections.abc import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.api.v1.medcenter.filters import ScheduleFilters
from core.apps.medcenter.entities import Schedule
from core.apps.medcenter.models import Schedule as ScheduleDTO
from core.apps.medcenter.services.base import BaseService


class ORMScheduleService(BaseService[ScheduleFilters, Schedule, ScheduleDTO]):
	filters = ScheduleFilters
	entity = Schedule
	model = ScheduleDTO

	@classmethod
	def _build_query(cls, filters: ScheduleFilters) -> Q:
		query = Q()
		
		return query

	def get_schedule_list(
		self,
		filters: ScheduleFilters,
		pagination: PaginationIn,
	) -> Iterable[Schedule]:
		return ORMScheduleService.get_list(
			filters=filters,
			pagination=pagination
		)

	def get_schedule_count(self, filters: ScheduleFilters) -> int:
		return ORMScheduleService.get_count(
			filters=filters
		)