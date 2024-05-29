from fastapi import FastAPI, Depends, Response
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from schemas.UsersSchema import UserWithRole
import models.Users as models
from config.database import engine, get_db
from sqlalchemy.orm import Session
from routes.AuthRouter import auth_router
import lib.auth.crud as AuthCrud

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins = ["*"],
  allow_methods = ["*"],
  allow_headers = ["*"]
)

models.Base.metadata.create_all(bind = engine)

app.include_router(auth_router)

@app.get("/users", response_model=list[UserWithRole])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  return AuthCrud.get_users(db, skip, limit)

@app.get("/users/{id_user}", response_model=UserWithRole)
async def get_users(id_user: int, db: Session = Depends(get_db)):
  return AuthCrud.get_user_by_id(db, id_user)