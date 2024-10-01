from pydantic import BaseModel
from typing import Optional
from typing import List

class UsersGroupBase(BaseModel):
  id_user_group: int
  id_user: int 
  id_group: int

class UserPermissionsUpdate(BaseModel):
    groups: List[int]