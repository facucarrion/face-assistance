from pydantic import BaseModel

class DevicesBase(BaseModel):
  id_device: int
  name: str
  id_config: int
  id_state: int
  state: str

  class Config:
    from_attributes = True

class DevicesCreate(BaseModel):
  name: str
  id_config: int
  id_state: int

class DevicesUpdate(BaseModel):
    name: str
    id_config: int
    id_state: int

    class Config:
        from_attributes = True
