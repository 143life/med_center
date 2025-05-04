
from collections.abc import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.api.v1.medcenter.filters import DoctorFilters
from core.apps.medcenter.entities.doctor import Doctor
from core.apps.medcenter.models import Doctor as DoctorDTO
from core.apps.medcenter.services.base import BaseService


class ORMDoctorService(BaseService[DoctorFilters, Doctor, DoctorDTO]):
	model = DoctorDTO
	filters = DoctorFilters
	entity = Doctor

	@classmethod
	def _build_query(cls, filters: DoctorFilters) -> Q:
			query = Q()

			return query

	def get_doctor_list(
			self,
			filters: DoctorFilters,
			pagination: PaginationIn,
	) -> Iterable[Doctor]:
		return ORMDoctorService.get_list(
			filters=filters,
			pagination=pagination
		)

	def get_doctor_count(self, filters: DoctorFilters) -> int:
		return ORMDoctorService.get_count(filters=filters)
