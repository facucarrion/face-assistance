from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.SchedulesExceptionsSchema import SchedulesExceptionsBase, ExceptionsCreate, ExceptionsUpdate
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

@schedule_exceptions_router.put("/{id_schedule_exception}", response_model=SchedulesExceptionsBase)
async def update_existing_schedules_exception(id_schedule_exception: int, schedules_exception_update: ExceptionsUpdate, db: Session = Depends(get_db)):
    schedules_exception = ExceptionsCrud.update_schedules_exceptions(db, id_schedule_exception, schedules_exception_update)
    return schedules_exception

@schedule_exceptions_router.delete("/{id_schedule_exception}")
async def delete_existing_schedule_exception(id_schedule_exception: int, db: Session = Depends(get_db)):
    schedules_exception = ExceptionsCrud.delete_schedules_exception(db, id_schedule_exception)
    return schedules_exception