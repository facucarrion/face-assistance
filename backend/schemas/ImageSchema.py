from pydantic import BaseModel

class ImageBase(BaseModel):
    image: str
    id_person: int