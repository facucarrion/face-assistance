from pydantic import BaseModel

class AssistanceBase(BaseModel):
    id_assistance: int
    id_person: int
    id_period: int
    date: str
    time: str

    class Config:
      from_attributes = True

class AssistanceCreate(BaseModel):
    id_person: int
    date: str
    time: str

class AssistanceUpdate(BaseModel):
    id_person: int
    date: str
    time: str

    class Config:
      from_attributes = True
