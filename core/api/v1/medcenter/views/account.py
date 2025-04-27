from django.http import HttpRequest

from ninja import Router

from core.api.schemas import ApiResponse
from core.api.v1.medcenter.schemas.person import PersonSchema
from core.apps.medcenter.services.person import (
    BasePersonService,
    ORMPersonService,
)


router = Router()


@router.get("/person/{person_id}", response=ApiResponse[PersonSchema])
def get_person(
    request: HttpRequest,
    person_id: int,
) -> ApiResponse[PersonSchema]:
    service: BasePersonService = ORMPersonService()
    person = service.get_person_by_id(person_id=person_id)
    if person is None:
        return ApiResponse(data={}, errors=["error404: Person not found"])
    return ApiResponse(data=PersonSchema.from_entity(person))
