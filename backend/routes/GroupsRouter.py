from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.GroupsSchemas import GroupsBase, GroupCreate, GroupUpdate
from config.database import get_db
from lib.groups.crud import get_group, create_group, update_group, delete_group

groups_router = APIRouter(
    prefix="/groups",
)

@groups_router.get("/", response_model=list[GroupsBase])
async def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = get_group(db, skip=skip, limit=limit)
    return groups

@groups_router.post("/", response_model=GroupsBase)
async def create_new_group(group: GroupCreate, db: Session = Depends(get_db)):
    return create_group(db, group)

@groups_router.put("/{id_group}", response_model=GroupsBase)
async def update_existing_group(id_group: int, group_update: GroupUpdate, db: Session = Depends(get_db)):
    db_group = update_group(db, id_group, group_update)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return db_group

@groups_router.delete("/{id_group}", response_model=GroupsBase)
async def delete_existing_group(id_group: int, db: Session = Depends(get_db)):
    db_group = delete_group(db, id_group)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return db_group

