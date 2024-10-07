from fastapi import Depends
from fastapi.routing import APIRouter
from schemas.TempImagesSchema import TempImagesCreate, TempImagesBase
from config.database import get_db
from lib.temp_images.crud import create_empty_temp_image, delete_temp_image

temp_images_router = APIRouter(
  prefix="/temp_images"
)

@temp_images_router.post("/create_empty_temp_image", response_model=TempImagesBase)
async def create_empty_temp_image_route(person: TempImagesCreate, db = Depends(get_db)):
  temp_image = create_empty_temp_image(db, person.id_person)
  return temp_image

@temp_images_router.delete("/{id_temp_images}", response_model=TempImagesBase)
async def delete_temp_image_route(id_temp_images: int, db = Depends(get_db)):
  temp_image = delete_temp_image(db, id_temp_images)
  return temp_image