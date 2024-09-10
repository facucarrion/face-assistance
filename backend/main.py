from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
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
from routes.ExceptionsRouter import schedule_excetions_router
from schemas.ImageSchema import ImageBase
from models.People import People

os.makedirs("public/uploads", exist_ok=True)

app = FastAPI()

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
app.include_router(schedule_excetions_router)


@app.post("/image/upload", response_model=dict)
async def upload_image(request: ImageBase, db: Session = Depends(get_db)):
  imgdata = base64.b64decode(request.image)
  filename = f"/uploads/{request.id_person}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpeg"

  with open(f"public/{filename}", 'wb') as f:
    f.write(imgdata)

  # update image field of request.id_person
  db_person = db.query(People).filter(
    People.id_person == request.id_person
  ).first()

  old_image = db_person.image
  db_person.image = filename
  db.commit()

  os.remove(f"public/{old_image}")

  return {
    "filename": filename
  }
