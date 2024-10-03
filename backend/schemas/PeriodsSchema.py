from pydantic import BaseModel
from typing import Optional

class PeriodsBase(BaseModel):
    id_period: int
    start_date: str
    end_date: str
    vacation_start: str
    vacation_end: str
    year: int

    class Config:
        from_attributes = True
            
class PeriodsCreate(BaseModel):
    start_date: str
    end_date: str
    vacation_start: str
    vacation_end: str
    year: int

class PeriodsUpdate(BaseModel):
    start_date: str
    end_date: str
    vacation_start: str
    vacation_end: str
    year: int

    class Config:
        from_attributes = True

