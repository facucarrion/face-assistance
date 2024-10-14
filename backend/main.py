from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import cv2
import base64
from datetime import datetime
from config.database import get_db
from sqlalchemy.orm import Session
from routes.AuthRouter import auth_router
from routes.GroupsRouter import groups_router
from routes.UsersRouter import users_router
from routes.PeopleRouter import people_router
from routes.SchedulesRouter import schedules_router
from routes.DaysRouter import days_router
from routes.ExceptionsRouter import schedule_exceptions_router
from routes.PeriodsRouter import periods_router
from routes.DevicesRouter import devices_router
from routes.StatesRouter import states_router
from routes.TempImagesRouter import temp_images_router
from schemas.ImageSchema import ImageBase
from schemas.AssistanceSchema import AssistanceCreate
from models.People import People
from models.Devices import Devices
from models.TempImages import TempImages
from models.Groups import Groups
from models.Assistance import Assistance


from lib.images.recognition import recognize_and_crop_image, compare_images
from lib.devices.crud import get_device_by_id
from lib.periods.crud import get_period_by_year

os.makedirs("public/uploads", exist_ok=True)
os.makedirs("temp/uploads", exist_ok=True)

app = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")
app.mount("/temp", StaticFiles(directory="temp/uploads"), name="temp_uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(groups_router)
app.include_router(users_router)
app.include_router(people_router)
app.include_router(schedules_router)
app.include_router(days_router)
app.include_router(schedule_exceptions_router)
app.include_router(periods_router)
app.include_router(devices_router)
app.include_router(states_router)
app.include_router(temp_images_router)

@app.post("/image/upload", response_model=dict)
async def upload_image(request: ImageBase, db: Session = Depends(get_db)):
    imgdata = base64.b64decode(request.image)
    filename = f"{request.id_person}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpeg"
    temp_file = f"temp/{filename}"

    with open(temp_file, "wb") as file:
        file.write(imgdata)

    # Llama a la función para reconocer y recortar la imagen
    new_image = recognize_and_crop_image(f"temp/{filename}", f"temp/uploads/{filename}")

    # Verifica si se detectó una cara
    if new_image["face_detected"]:
        cv2.imwrite(new_image['destine_path'], new_image['cropped_face'])

        db_temp_image = (db
            .query(TempImages)
            .filter(TempImages.id_person == request.id_person).first())
        old_image = db_temp_image.image
        db_temp_image.image = f"temp/{filename}"
        db.commit()

        db_device = (db
            .query(Devices)
            .join(Groups, Groups.id_device == Devices.id_device)
            .join(People, People.id_group == Groups.id_group)
            .filter(People.id_person == request.id_person).first())
        db_device.id_state = 1
        db.commit()

        if old_image:
            os.remove(old_image)

        os.remove(temp_file)

        return {
            "filename": filename,
            "temp_file": temp_file,
            "message": "Image uploaded and face detected",
            "success": True
        }
    else:
        os.remove(temp_file)
        return {
            "message": "No face detected in the image",
            "success": False
        }
    
@app.post("/assistance/new", response_model=dict)
async def new_assistance(request: AssistanceCreate, db: Session = Depends(get_db)):
    imgdata = base64.b64decode(request.image)
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpeg"
    temp_file = f"temp/{filename}"

    with open(temp_file, "wb") as file:
        file.write(imgdata)

    # Llama a la función para reconocer y recortar la imagen
    new_image = recognize_and_crop_image(f"temp/{filename}", f"temp/uploads/{filename}")

    # Verifica si se detectó una cara
    if new_image["face_detected"]:
        cv2.imwrite(new_image['destine_path'], new_image['cropped_face'])

        db_people = (db
            .query(People)
            .join(Groups, Groups.id_group == People.id_group).join(Devices, Devices.id_device == Groups.id_device)
            .filter(Devices.id_config == request.id_config)
            .all()
        )

        is_coincident = False
        coincident_person = None

        for people in db_people:
            if (people.image == None):
                continue

            # change /temp/image to /temp/uploads/image
            image_to_compare = people.image.replace("temp", "temp/uploads")
            coincidence = compare_images(image_to_compare, new_image['destine_path'])

            if (coincidence > 80):
                is_coincident = True
                coincident_person = people
                break

        os.remove(temp_file)

        if (is_coincident):
            db_assistance = Assistance(
                id_person = coincident_person.id_person,
                id_period = get_period_by_year(db, datetime.now().year)["id_period"],
                date = datetime.now().strftime("%Y-%m-%d"),
                time = datetime.now().strftime("%H:%M:%S")
            )
            db.add(db_assistance)
            db.commit()

            return {
                "message": "Assistance registered",
                "success": True,
                "coincidence": coincidence,
                "assistance": db_assistance.id_assistance
            }
        
        return {
            "message": "No",
            "success": False,
            "coincidence": coincidence
        }
    else:
        return {
            "message": "No face detected in the image",
            "success": False
        }