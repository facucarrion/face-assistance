from pydantic import BaseModel

class UserBase(BaseModel):
  id_user: int
  username: str
  password: str
  id_rol: int

  class Config:
    orm_mode = True

class UserCreate(UserBase):
  pass

class RolBase(BaseModel):
  id_rol: int
  rol: str

  class Config:
    orm_mode = True

class RolCreate(RolBase):
  pass