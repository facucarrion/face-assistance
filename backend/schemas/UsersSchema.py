from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
  id_user: int
  username: str

  class Config:
    from_attributes = True


class UserWithRole(UserBase):
    id_rol: int
    rol: str
    
class UserCreate(BaseModel):
    username: str
    password: str
    repeat_password: str
    id_rol: int

class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    id_rol: Optional[int]



class RolBase(BaseModel):
    id_rol: int
    rol: str

    class Config:
        from_attributes = True

class RolCreate(RolBase):
    pass


