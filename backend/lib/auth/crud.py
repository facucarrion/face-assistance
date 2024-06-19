from sqlalchemy.orm import Session

from models.Users import User, Roles
from schemas.UsersSchema import UserCreate, UserUpdate
from passlib.context import CryptContext

def get_users(db: Session, skip: int = 0, limit: int = 100):
  users = (db
    .query(
      User.id_user,
      User.username,
      Roles.rol
    )
    .join(Roles, User.id_rol == Roles.id_rol)
    .offset(skip)
    .limit(limit)
    .all()
  )
  return users

def get_user_by_id(db: Session, id_user: int):
  user = (db
    .query(User.id_user, User.username, Roles.rol)
    .join(Roles, User.id_rol == Roles.id_rol)
    .filter(User.id_user == id_user)
    .first()
  )
  
  return user

def get_user_by_username(db: Session, username: str):
  user = (db
    .query(User.id_user, User.username, User.password, Roles.rol)
    .join(Roles, User.id_rol == Roles.id_rol)
    .filter(User.username == username)
    .first()
  )

  return user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password) 

def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, password=hashed_password, id_rol=user.id_rol)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  
    return db_user

def update_user(db: Session, id_user: int, user_update: UserUpdate):
    user = db.query(User).filter(User.id_user == id_user).first()
    if not user:
        return None
    for key, value in user_update.dict(exclude_unset=True).items():
        if key == "password" and value is not None:
            value = hash_password(value)
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, id_user: int):
    user = db.query(User).filter(User.id_user == id_user).first()
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user