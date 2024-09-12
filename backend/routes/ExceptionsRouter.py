from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.SchedulesExceptionsSchema import SchedulesExceptionsBase, ExceptionsCreate
from config.database import get_db
import lib.schedule_exceptions.crud as ExceptionsCrud

schedule_exceptions_router = APIRouter(
    prefix="/schedule_exceptions",
)

@schedule_exceptions_router.post("/")
async def create_new_exceptions(schedules_excetions: ExceptionsCreate, db: Session = Depends(get_db)):
    return ExceptionsCrud.create_exceptions(db, schedules_excetions)

@schedule_exceptions_router.get("/{id_group}")
async def get_schedule_exceptions_by_group(id_group: int, db: Session = Depends(get_db)):
    schedules_exceptions = ExceptionsCrud.get_schedule_exceptions_by_group(db=db, id_group=id_group)
    return schedules_exceptions