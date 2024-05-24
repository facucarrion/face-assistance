from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
  id_user: int
  username: str

  class Config:
    from_attributes = True

class UserCreate(UserBase):
  pass

class UserWithRole(BaseModel):
  id_user: int
  username: str
  rol: str

class RolBase(BaseModel):
  id_rol: int
  rol: str

  class Config:
    from_attributes = True

class RolCreate(RolBase):
  pass