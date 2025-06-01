from django.db.models import Q

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
