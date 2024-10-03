from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.PeriodsSchema import PeriodsBase, PeriodsCreate, PeriodsUpdate
from config.database import get_db
import lib.periods.crud as PeriodsCrud

periods_router = APIRouter(
    prefix="/periods",
)

@periods_router.post("/")
async def create_new_periods(periods: PeriodsCreate, db: Session = Depends(get_db)):
    return PeriodsCrud.create_periods(db, periods)

@periods_router.get("/{id_group}")
async def get_schedules_by_group(id_group: int, db: Session = Depends(get_db)):
    schedules = crud_get_schedules_by_group(db=db, id_group=id_group)
    return schedules
