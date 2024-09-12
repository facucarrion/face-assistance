from pydantic import BaseModel

class DaysBase(BaseModel):
    id_day: int
    day: str
    
    class Config:
        from_attributes = True