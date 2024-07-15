from pydantic import BaseModel
from typing import Optional

from pydantic import BaseModel

class GroupsBase(BaseModel):
    id_group: int
    name: str

    class Config:
        from_attributes = True

class GroupCreate(BaseModel):
    name: str

class GroupUpdate(BaseModel):
    name: str

