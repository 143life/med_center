from collections.abc import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.api.v1.medcenter.filters import AppointmentFilters
from core.apps.medcenter.entities.appointment import Appointment
from core.apps.medcenter.models.appointment import (
    Appointment as AppointmentDTO,
)
from core.apps.medcenter.services.base import BaseService


class ORMAppointmentService(
    BaseService[AppointmentFilters, Appointment, AppointmentDTO],
):
    filters = AppointmentFilters
    model = AppointmentDTO
    entity = Appointment

    @classmethod
    def _build_query(cls, filters: AppointmentFilters) -> Q:
        query = Q()

        return query

    def get_appointment_list(
        filters: AppointmentFilters,
        pagination: PaginationIn,
    ) -> Iterable[Appointment]:
        return ORMAppointmentService.get_list(
            filters=filters,
            pagination=pagination,
        )

    def get_appointment_count(filters: AppointmentFilters) -> int:
        return ORMAppointmentService.get_count(filters=filters)
