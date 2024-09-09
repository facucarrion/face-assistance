from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.SchedulesSchema import SchedulesBase, SchedulesCreate
from config.database import get_db
from lib.schedules.crud import create_schedules, get_all_days

schedules_router = APIRouter(
    prefix="/schedules",
)

@schedules_router.post("/")
async def create_new_schedules(schedules: SchedulesCreate, db: Session = Depends(get_db)):
    return create_schedules(db, schedules)