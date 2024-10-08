from pydantic import BaseModel
from typing import Optional
from schemas.PeopleSchema import PeopleWithAssistance

class GroupsBase(BaseModel):
    id_group: int
    name: str
    id_device: Optional[int] = None

    class Config:
        from_attributes = True

class GroupsWithPeople(GroupsBase):
    people: list[PeopleWithAssistance]

class GroupCreate(BaseModel):
    name: str
    id_device: str

class GroupUpdate(BaseModel):
    name: str
    id_device: str

class GroupTransfer(BaseModel):
    from_group_id: int
    to_group_id: int
