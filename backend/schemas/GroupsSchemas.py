from pydantic import BaseModel
from typing import Optional

class GroupsBase(BaseModel):
  id_group: int
  name: str

  # class Config:
  #   from_attributes = True
  class Config:
    orm_mode = True  

class GroupCreate(BaseModel):
    name: str
