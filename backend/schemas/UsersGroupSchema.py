from pydantic import BaseModel
from typing import Optional

class UsersGroupBase(BaseModel):
  id_user_group: int
  id_user: int 
  id_group: int
