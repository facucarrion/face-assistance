from pydantic import BaseModel
from typing import Optional
from schemas.PeopleSchema import PeopleBase

from pydantic import BaseModel

class GroupsBase(BaseModel):
    id_group: int
    name: str

    class Config:
        from_attributes = True

class GroupsWithPeople(GroupsBase):
    people: list[PeopleBase]

class GroupCreate(BaseModel):
    name: str

class GroupUpdate(BaseModel):
    name: str

