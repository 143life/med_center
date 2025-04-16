from datetime import datetime
from pydantic import BaseModel

class PersonSchema(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    date_birth: datetime

PersonListSchema = list[PersonSchema]