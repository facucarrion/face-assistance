from fastapi import FastAPI, Depends
from schemas.UsersSchema import UserBase, UserWithRole
import models.Users as models
from config.database import engine, SessionLocal
from sqlalchemy.orm import Session
from routes.AuthRouter import auth_router

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

app.include_router(auth_router)

@app.get("/users", response_model=list[UserWithRole])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  users = (db
      .query(
        models.User.id_user,
        models.User.username,
        models.Roles.rol
      )
      .join(models.Roles, models.User.id_rol == models.Roles.id_rol)
      .offset(skip)
      .limit(limit)
      .all()
    )
  return users

@app.get("/users/{id_user}", response_model=UserBase)
async def get_users(id_user: int, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id_user == id_user).first()
  return user