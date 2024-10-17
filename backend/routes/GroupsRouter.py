from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.GroupsSchemas import GroupsBase, GroupCreate, GroupUpdate, GroupsWithPeople, GroupTransfer
from schemas.PeopleSchema import PeopleBase
from config.database import get_db
from lib.groups.crud import get_groups, get_group_by_id as crud_get_group_by_id, get_group_with_people_by_id, create_group, update_group, delete_group, get_people_in_group, update_people_group
from lib.people.crud import delete_people_by_group
from lib.schedule_exceptions.crud import delete_schedule_exception_by_group
from lib.schedules.crud import delete_schedule_by_group
from lib.assistance.crud import delete_assistance_by_group
from lib.users_group.crud import delete_usergroup_by_group

groups_router = APIRouter(
    prefix="/groups",
)

@groups_router.get("/", response_model=list[GroupsBase])
async def read_groups(skip: int = 0, limit: int = 100, id_user: int = 0, db: Session = Depends(get_db)):
  groups = get_groups(db, skip=skip, limit=limit, id_user=id_user)
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
  return db_group

@groups_router.delete("/{id_group}", response_model=GroupsBase)
async def delete_existing_group(id_group: int, db: Session = Depends(get_db)):
    db_assistance = delete_assistance_by_group(db, id_group)
    db_people = delete_people_by_group(db, id_group)
    db_schedules = delete_schedule_by_group(db, id_group)
    db_schedules_exceptions = delete_schedule_exception_by_group(db, id_group)
    db_user_group = delete_usergroup_by_group(db, id_group)
    db_group = delete_group(db, id_group)
    return db_group

@groups_router.get("/{id_group}/people", response_model=list[PeopleBase])
async def get_people_in_group(id_group: int, db: Session = Depends(get_db)):
  return get_people_in_group(db, id_group)

@groups_router.post("/transfer")
async def transfer_people_to_new_group(groups: GroupTransfer, db: Session = Depends(get_db)):
    people_in_group = get_people_in_group(db, groups.from_group_id)
    updated_people = update_people_group(db, groups.from_group_id, groups.to_group_id)
    return {"message": f"{len(updated_people)} personas trasladadas al nuevo curso."}
