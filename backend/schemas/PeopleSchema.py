from pydantic import BaseModel

class PersonCreate(BaseModel):
    firstname: str
    lastname: str
    document: str
    image: str
    id_group: int

    class Config:
        orm_mode = True
