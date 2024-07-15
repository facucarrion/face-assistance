from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel

class PeopleBase(BaseModel):
    id_person: int
    firstname: str
    lastname: str
    document: str
    image: str
    id_group: int

    class Config:
        from_attributes = True

class PeopleCreate(BaseModel):
    firstname: str
    lastname: str
    document: str
    image: str
    id_group: int

class PeopleUpdate(BaseModel):
    firstname: str
    lastname: str
    document: str
    image: str
    id_group: int

    class Config:
        from_attributes = True