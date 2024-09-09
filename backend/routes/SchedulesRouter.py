from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.SchedulesSchema import SchedulesBase, SchedulesCreate
from config.database import get_db
from lib.schedules.crud import create_schedules, get_schedules_by_group as crud_get_schedules_by_group

schedules_router = APIRouter(
    prefix="/schedules",
)

@schedules_router.post("/")
async def create_new_schedules(schedules: SchedulesCreate, db: Session = Depends(get_db)):
    return create_schedules(db, schedules)

@schedules_router.get("/{id_group}")
async def get_schedules_by_group(id_group: int, db: Session = Depends(get_db)):
    schedules = crud_get_schedules_by_group(db=db, id_group=id_group)
    return schedules
