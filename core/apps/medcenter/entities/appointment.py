from dataclasses import dataclass

from core.apps.medcenter.entities.specialization import Specialization
from core.apps.medcenter.entities.ticket import Ticket


@dataclass
class Appointment:
    ticket: "Ticket"
    specialization: "Specialization"
    completed: bool
