from django.http import HttpRequest

from ninja import (
    Query,
    Router,
)

from core.api.filters import (
    PaginationIn,
    PaginationOut,
)
from core.api.schemas import (
    ApiResponse,
    ListPaginatedResponse,
)
from core.api.v1.medcenter.filters import (
    DoctorFilters,
    PersonFilters,
    SpecializationFilters,
)
from core.api.v1.medcenter.schemas.doctor import DoctorSchema
from core.api.v1.medcenter.schemas.specialization import SpecializationSchema
from core.api.v1.medcenter.views.account import router as account_router
from core.apps.medcenter.services.doctor import (
    BaseDoctorService,
    ORMDoctorService,
)
from core.apps.medcenter.services.person import (
    BasePersonService,
    ORMPersonService,
)
from core.apps.medcenter.services.specialization import (
    BaseSpecializationService,
    ORMSpecializationService,
)

from .schemas.person import PersonSchema


router = Router(tags=["medcenter"])
router.add_router("account", account_router)


@router.get(
    "/person",
    response=ApiResponse[ListPaginatedResponse[PersonSchema]],
)
def get_person_list_handler(
    request: HttpRequest,
    filters: Query[PersonFilters],
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[PersonSchema]]:
    service: BasePersonService = ORMPersonService()
    person_list = service.get_person_list(
        filters=filters,
        pagination=pagination_in,
    )
    person_count = service.get_person_count(filters=filters)
    items = [PersonSchema.from_entity(obj) for obj in person_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=person_count,
    )

    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out),
    )


@router.get(
    "/doctor",
    response=ApiResponse[ListPaginatedResponse[DoctorSchema]],
)
def get_doctor_list_handler(
    request: HttpRequest,
    filters: Query[DoctorFilters],
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[DoctorSchema]]:
    service: BaseDoctorService = ORMDoctorService()
    doctor_list = service.get_doctor_list(
        filters=filters,
        pagination=pagination_in,
    )
    doctor_count = service.get_doctor_count(filters=filters)
    items = [DoctorSchema.from_entity(obj) for obj in doctor_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=doctor_count,
    )

    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out),
    )


@router.get(
    "/specialization",
    response=ApiResponse[ListPaginatedResponse[SpecializationSchema]],
)
def get_specialization_list_handler(
    request: HttpRequest,
    filters: Query[SpecializationFilters],
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[SpecializationSchema]]:
    service: BaseSpecializationService = ORMSpecializationService()
    specialization_list = service.get_specialization_list(
        filters=filters,
        pagination=pagination_in,
    )
    specialization_count = service.get_specialization_count(filters=filters)
    items = [
        SpecializationSchema.from_entity(obj) for obj in specialization_list
    ]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=specialization_count,
    )

    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out),
    )
