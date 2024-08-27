from pydantic import BaseModel

class ImageBase(BaseModel):
    image: str