from django.http import HttpRequest
from ninja import Router
from .schemas.person import PersonListSchema

router = Router(tags=['medcenter'])

@router.get('/person', response=PersonListSchema)
def get_person_list_handler(request:HttpRequest) -> PersonListSchema:
    return []