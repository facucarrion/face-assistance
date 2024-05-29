from pydantic import BaseModel

class ApiMessageSchema(BaseModel):
  success: bool
  status: int
  message: str
  data: dict = {}