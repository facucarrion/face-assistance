from pydantic import BaseModel

class LoginSchema(BaseModel):
  username: str
  password: str

class RegisterSchema(BaseModel):
  username: str
  password: str
  repeat_password: str
  id_rol: int