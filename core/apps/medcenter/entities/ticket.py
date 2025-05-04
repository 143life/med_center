from dataclasses import dataclass
from datetime import datetime

from core.apps.medcenter.entities.person import Person


@dataclass
class Ticket:
    person: "Person"
    datetime: datetime
    number: int
    completed: bool
