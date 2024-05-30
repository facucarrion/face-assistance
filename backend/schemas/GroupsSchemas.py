from pydantic import BaseModel
from typing import Optional

class GroupsBase(BaseModel):
  id_group: int
  name: str

  class Config:
    from_attributes = True