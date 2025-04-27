from core.apps.medcenter.services.person import ORMPersonService


def person_service() -> ORMPersonService:
    return ORMPersonService()
