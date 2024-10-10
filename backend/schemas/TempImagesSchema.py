from pydantic import BaseModel

class TempImagesBase(BaseModel):
  id_temp_images: int
  id_person: int
  image: str

  class Config:
    from_attributes = True

class TempImagesCreate(BaseModel):
  id_person: int

class TempImagesUpdate(BaseModel):
  image: str