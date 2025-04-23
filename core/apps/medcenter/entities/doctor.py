from dataclasses import dataclass

from core.apps.medcenter.entities.person import Person
from core.apps.medcenter.entities.specialization import Specialization


@dataclass
class Doctor:
    person: "Person"
    specialization: "Specialization"
