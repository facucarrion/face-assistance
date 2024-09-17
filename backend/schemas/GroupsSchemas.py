from pydantic import BaseModel
from schemas.PeopleSchema import PeopleWithAssistance

class GroupsBase(BaseModel):
    id_group: int
    name: str

    class Config:
        from_attributes = True

class GroupsWithPeople(GroupsBase):
    people: list[PeopleWithAssistance]

class GroupCreate(BaseModel):
    name: str

class GroupUpdate(BaseModel):
    name: str

class GroupTransfer(BaseModel):
    from_group_id: int
    to_group_id: int

