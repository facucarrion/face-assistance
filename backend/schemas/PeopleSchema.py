from pydantic import BaseModel
from typing import Optional

class PeopleBase(BaseModel):
    id_person: int
    firstname: str
    lastname: str
    document: str
    image: Optional[str] = None
    id_group: int

    class Config:
        from_attributes = True

class PeopleWithAssistance(BaseModel):
    id_person: int
    firstname: str
    lastname: str
    document: str
    image: Optional[str] = None
    id_group: int
    assistance: dict

    class Config:
        from_attributes = True

class PeopleCreate(BaseModel):
    firstname: str
    lastname: str
    document: str
    id_group: int

class PeopleUpdate(BaseModel):
    firstname: str
    lastname: str
    document: str
    id_group: int

    class Config:
        from_attributes = True