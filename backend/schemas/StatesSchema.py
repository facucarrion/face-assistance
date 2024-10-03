from pydantic import BaseModel

class StatesBase(BaseModel):
  id_state: int
  state: str

  class Config:
    from_attributes = True