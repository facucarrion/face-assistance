from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from schemas.UsersSchema import UserWithRole, UserCreate
from config.database import get_db
from sqlalchemy.orm import Session
from routes.AuthRouter import auth_router
from routes.GroupsRouter import groups_router
import lib.auth.crud as AuthCrud
import lib.groups.crud as GroupCrud
from schemas.GroupsSchemas import GroupsBase, GroupCreate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(groups_router)

@app.get("/users", response_model=list[UserWithRole])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return AuthCrud.get_users(db, skip, limit)

@app.get("/users/{id_user}", response_model=UserWithRole)
async def get_users(id_user: int, db: Session = Depends(get_db)):
    return AuthCrud.get_user_by_id(db, id_user)

@app.get("/groups", response_model=list[GroupsBase])
async def get_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return GroupCrud.get_group(db, skip, limit)

@app.post("/api/groups")
async def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    return GroupCrud.create_group(db=db, group=group)
