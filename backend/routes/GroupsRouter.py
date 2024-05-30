from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.GroupsSchemas import GroupsBase
from config.database import get_db
from lib.groups.crud import get_group

groups_router = APIRouter(
    prefix="/groups",
)


@groups_router.get("/homepage", response_model=list[GroupsBase])
async def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = get_group(db, skip=skip, limit=limit)
    return groups