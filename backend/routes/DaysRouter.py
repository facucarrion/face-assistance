from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.DaysSchema import DaysBase
from config.database import get_db
from lib.schedules.crud import create_schedules, get_all_days


days_router = APIRouter(
    prefix="/days",
)

@days_router.get("/", response_model=List[DaysBase])
async def read_days(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    days = get_all_days(db, skip=skip, limit=limit)
    return days