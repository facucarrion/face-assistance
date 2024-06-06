from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.GroupsSchemas import GroupsBase, GroupCreate
from config.database import get_db
from lib.groups.crud import get_group, create_group

groups_router = APIRouter(
    prefix="/groups",
)

@groups_router.get("/homepage", response_model=list[GroupsBase])
async def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = get_group(db, skip=skip, limit=limit)
    return groups

@groups_router.post("/", response_model=GroupsBase)
async def create_new_group(group: GroupCreate, db: Session = Depends(get_db)):
    return create_group(db, group)

