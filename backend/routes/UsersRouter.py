from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.UsersSchema import UserBase, UserCreate, UserUpdate, UserWithRole, RolBase
from config.database import get_db
from lib.auth.crud import get_users, create_user, update_user, delete_user
from lib.users_group.crud import delete_usergroup_by_user
from models.Users import Roles

users_router = APIRouter(
    prefix="/users",
)

@users_router.get("/", response_model=list[UserWithRole])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@users_router.post("/", response_model=UserBase)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return db_user

@users_router.put("/{id_user}", response_model=UserBase)
async def update_user_details(id_user: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = update_user(db, id_user, user_update)
    return db_user

@users_router.delete("/{id_user}", response_model=UserBase)
async def delete_user_account(id_user: int, db: Session = Depends(get_db)):
    db_user_group = delete_usergroup_by_user(db, id_user)
    db_user = delete_user(db, id_user)
    return db_user

@users_router.get("/roles/", response_model=list[RolBase])
async def get_roles(db: Session = Depends(get_db)):
    roles = db.query(Roles).all()
    return roles