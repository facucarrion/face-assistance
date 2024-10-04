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
from schemas.ImageSchema import ImageBase
from models.People import People

from lib.images.recognition import recognize_and_crop_image

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

@app.post("/image/upload", response_model=dict)
async def upload_image(request: ImageBase, db: Session = Depends(get_db)):
    imgdata = base64.b64decode(request.image)
    filename = f"{request.id_person}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpeg"
    temp_file = f"temp/uploads/{filename}"

    print(filename)
    print(temp_file)

    with open(temp_file, "wb") as file:
        file.write(imgdata)

    new_image = recognize_and_crop_image(f"temp/uploads/{filename}", f"public/uploads/{filename}")

    print(new_image["destine_path"])

    cv2.imwrite(new_image['destine_path'], new_image['cropped_face'])

    person = db.query(People).filter(People.id_person == request.id_person).first()
    old_image = person.image
    person.image = f"uploads/{filename}"
    db.commit()

    if old_image:
        os.remove(f"public/{old_image}")

    os.remove(temp_file)

    return {
        "filename": filename,
        "temp_file": temp_file
    }
