from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.GroupsSchemas import GroupsBase, GroupCreate, GroupUpdate, GroupsWithPeople
from schemas.PeopleSchema import PeopleBase
from config.database import get_db
from lib.groups.crud import get_groups, get_group_by_id as crud_get_group_by_id, get_group_with_people_by_id, create_group, update_group, delete_group, get_people_in_group
from lib.people.crud import delete_people_by_group

groups_router = APIRouter(
    prefix="/groups",
)

@groups_router.get("/", response_model=list[GroupsBase])
async def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = get_groups(db, skip=skip, limit=limit)
    return groups

@groups_router.get("/{id_group}", response_model=GroupsWithPeople)
async def get_group_by_id(id_group: int, db: Session = Depends(get_db)):
    group = get_group_with_people_by_id(db, id_group)
    return group

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
    db_people = delete_people_by_group(db, id_group)
    db_group = delete_group(db, id_group)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return db_group

@groups_router.get("/{id_group}/people", response_model=list[PeopleBase])
async def get_people_in_group(id_group: int, db: Session = Depends(get_db)):
    return get_people_in_group(db, id_group)