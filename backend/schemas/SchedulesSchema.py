from pydantic import BaseModel
from typing import Optional

class SchedulesBase(BaseModel):
    id_schedule: int
    id_group: int
    id_day: int
    start_time: str
    end_time: str

    class Config:
        from_attributes = True

class SchedulesCreate(BaseModel):
    id_day: int
    start_time: str
    end_time: str

class SchedulesUpdate(BaseModel):
    id_day: int
    start_time: str
    end_time: str

    class Config:
        from_attributes = True