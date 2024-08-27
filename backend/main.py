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
import lib.auth.crud as AuthCrud
import lib.groups.crud as GroupCrud
import lib.people.crud as PeopleCrud
import lib.assistance.crud as AssistanceCrud
from schemas.GroupsSchemas import GroupsBase, GroupCreate, GroupUpdate
from schemas.UsersSchema import UserWithRole, UserCreate, UserUpdate
from schemas.PeopleSchema import PeopleBase, PeopleCreate, PeopleUpdate, PeopleWithAnnualAssistance
from schemas.ImageSchema import ImageBase

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

@app.post("/image/upload", response_model=dict)
async def upload_image(request: ImageBase):
    imgdata = base64.b64decode(request.image)
    filename = f"public/uploads/{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpeg"

    with open(filename, 'wb') as f:
        f.write(imgdata)

    return {
        "filename": filename
    }
    

@app.get("/users", response_model=list[UserWithRole])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return AuthCrud.get_users(db, skip, limit)

@app.get("/users/{id_user}", response_model=UserWithRole)
async def get_users(id_user: int, db: Session = Depends(get_db)):
    return AuthCrud.get_user_by_id(db, id_user)

@app.post("/users", response_model=UserWithRole)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return AuthCrud.create_user(db=db, user=user)

@app.put("/users/{id_user}", response_model=UserWithRole)
async def update_user(id_user: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    return AuthCrud.update_user(db=db, id_user=id_user, user_update=user_update)

@app.delete("/users/{id_user}", response_model=UserWithRole)
async def delete_user(id_user: int, db: Session = Depends(get_db)):
    return AuthCrud.delete_user(db=db, id_user=id_user)

@app.get("/groups", response_model=list[GroupsBase])
async def get_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
     return GroupCrud.get_groups(db, skip, limit)

@app.post("/groups", response_model=GroupsBase)
async def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    return GroupCrud.create_group(db=db, group=group)

@app.put("/groups/{id_group}", response_model=GroupsBase)
async def update_group(id_group: int, group_update: GroupUpdate, db: Session = Depends(get_db)):
    return GroupCrud.update_group(db=db, id_group=id_group, group_update=group_update)

@app.delete("/groups/{id_group}", response_model=GroupsBase)
async def delete_group(id_group: int, db: Session = Depends(get_db)):
    return GroupCrud.delete_group(db=db, id_group=id_group)

@app.get("/people", response_model=list[PeopleBase])
async def get_people(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
     return PeopleCrud.get_people(db, skip, limit)

@app.post("/people", response_model=PeopleBase)
async def create_people(people: PeopleCreate, db: Session = Depends(get_db)):
    return PeopleCrud.create_people(db=db, people=people)

@app.put("/people/{id_person}", response_model=PeopleBase)
async def update_people(id_person: int, people_update: PeopleUpdate, db: Session = Depends(get_db)):
    return PeopleCrud.update_people(db=db, id_person=id_person, people_update=people_update)

@app.delete("/people/{id_person}", response_model=PeopleBase)
async def delete_people(id_person: int, db: Session = Depends(get_db)):
    return PeopleCrud.delete_people(db=db, id_person=id_person)

@app.get("/groups/{id_group}/people", response_model=list[PeopleBase])
async def get_people_in_group(id_group: int, db: Session = Depends(get_db)):
    return GroupCrud.get_people_in_group(db=db, id_group=id_group)
