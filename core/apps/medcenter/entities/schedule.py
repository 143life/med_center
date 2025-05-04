from dataclasses import dataclass
from datetime import datetime


@dataclass
class Schedule:
    datetime_begin: datetime
    datetime_end: datetime
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    sunday: bool
