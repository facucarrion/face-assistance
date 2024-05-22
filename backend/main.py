from fastapi import FastAPI, Depends
from schemas.Users import UserBase, RolBase
import models.Users as models
from config.database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


@app.get("/users", response_model=list[UserBase])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  users = (db
      .query(models.User)
      .join(models.Roles, models.Roles.id_rol == models.User.id_rol)
      .offset(skip)
      .limit(limit)
      .all()
    )
  return users

@app.get("/users/{id_user}", response_model=UserBase)
async def get_users(id_user: int, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id_user == id_user).first()
  return user