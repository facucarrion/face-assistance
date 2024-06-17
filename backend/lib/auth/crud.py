
from sqlalchemy.orm import Session

from models.Users import User, Roles
from schemas.UsersSchema import UserCreate, UserUpdate

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

def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    user = User(username=user.username, password=hashed_password, id_rol=user.id_rol)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, id_user: int, user_update: UserUpdate):
    user = db.query(User).filter(User.id_user == id_user).first()
    if not user:
        return None
    for key, value in user_update.dict(exclude_unset=True).items():
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
