from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.UsersSchema import UserBase, UserCreate, UserUpdate, UserWithRole, RolBase
from schemas.GroupsSchemas import GroupsBase
from schemas.UsersGroupSchema import UsersGroupBase, UserPermissionsUpdate
from config.database import get_db
from lib.auth.crud import get_users, create_user, update_user, delete_user
from lib.users_group.crud import delete_usergroup_by_user
from models.Users import Roles, User
from models.Groups import Groups
from models.UsersGroup import UsersGroup
from typing import List

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

@users_router.get("/{id_user}/permissions", response_model=List[GroupsBase])
async def get_user_permissions(id_user: int, db: Session = Depends(get_db)):
    user_groups = db.query(UsersGroup).filter(UsersGroup.id_user == id_user).all()
    group_ids = [ug.id_group for ug in user_groups]
    groups = db.query(Groups).filter(Groups.id_group.in_(group_ids)).all()
    return groups

@users_router.put("/{id_user}/permissions")
async def update_user_permissions(id_user: int, permissions: UserPermissionsUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id_user == id_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar que todos los grupos (cursos) existen
    valid_groups = db.query(Groups).filter(Groups.id_group.in_(permissions.groups)).all()
    if len(valid_groups) != len(permissions.groups):
        raise HTTPException(status_code=400, detail="Algunos grupos (cursos) no existen")

    # Eliminar asociaciones existentes
    delete_usergroup_by_user(db, id_user)

    # Añadir nuevas asociaciones
    for group_id in permissions.groups:
        user_group = UsersGroup(id_user=id_user, id_group=group_id)
        db.add(user_group)
    db.commit()

    return