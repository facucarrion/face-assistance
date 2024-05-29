from sqlalchemy.orm import Session

from models.Users import User, Roles

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