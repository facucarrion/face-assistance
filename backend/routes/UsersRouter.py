from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.UsersSchema import UserBase, UserCreate, UserUpdate, UserWithRole
from config.database import get_db
from lib.auth.crud import get_users, create_user, update_user, delete_user

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
    if db_user is None:
        raise HTTPException(status_code=400, detail="User already exists")
    return db_user

@users_router.put("/{id_user}", response_model=UserBase)
async def update_user_details(id_user: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = update_user(db, id_user, user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@users_router.delete("/{id_user}", response_model=UserBase)
async def delete_user_account(id_user: int, db: Session = Depends(get_db)):
    db_user = delete_user(db, id_user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

