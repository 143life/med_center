import pytest

from core.apps.medcenter.services.person import ORMPersonService


@pytest.mark.django_db
def test_person_count(person_service: ORMPersonService):
    assert True


@pytest.mark.django_db
def test_person_search():
    assert True
