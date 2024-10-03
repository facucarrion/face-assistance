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

@periods_router.put("/{id_periods}")
async def update_periods(id_period: int, periods_update: PeriodsUpdate, db: Session = Depends(get_db)):
    periods = PeriodsCrud.update_periods(db, id_period, periods_update)
    return periods
