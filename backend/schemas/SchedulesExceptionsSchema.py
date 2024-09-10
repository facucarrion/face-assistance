from pydantic import BaseModel
from typing import Optional

class SchedulesExceptionsBase(BaseModel):
    id_schedule_exceptions: int
    id_group: int
    date: str
    is_class: bool
    start_time: str
    end_time: str

    class Config:
        from_attributes = True

class ExceptionsCreate(BaseModel):
    id_group: int
    date: str
    is_class: bool
    start_time: str
    end_time: str