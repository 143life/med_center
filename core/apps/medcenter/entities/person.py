from dataclasses import dataclass
from datetime import datetime


@dataclass
class Person:
    """
    Domain entity for collect data
    from different sources
    """

    id: int
    first_name: str
    last_name: str
    patronymic: str
    date_birth: datetime
