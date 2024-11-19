from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.SchedulesExceptionsSchema import ExceptionsCreate, ExceptionsUpdate
from config.database import get_db
import lib.schedule_exceptions.crud as ExceptionsCrud

schedule_exceptions_router = APIRouter(
    prefix="/schedule_exceptions",
)

@schedule_exceptions_router.post("/")
async def create_new_exceptions(schedules_exception: ExceptionsCreate, db: Session = Depends(get_db)):
    if ExceptionsCrud.can_create_schedule_exception_by_group_date(db, schedules_exception.date, schedules_exception.id_group) == False:
        raise HTTPException(status_code=400, detail="Schedule exception already exists")
    return ExceptionsCrud.create_exceptions(db, schedules_exception)

@schedule_exceptions_router.get("/{id_group}")
async def get_schedule_exceptions_by_group(id_group: int, db: Session = Depends(get_db)):
    schedules_exceptions = ExceptionsCrud.get_schedule_exceptions_by_group(db=db, id_group=id_group)
    return schedules_exceptions

@schedule_exceptions_router.put("/{id_schedule_exception}")
async def update_existing_schedules_exception(id_schedule_exception: int, schedules_exception_update: ExceptionsUpdate, db: Session = Depends(get_db)):
    if ExceptionsCrud.can_update_schedule_exception_by_group_date(db, schedules_exception_update.date, schedules_exception_update.id_group, id_schedule_exception) == False:
        raise HTTPException(status_code=400, detail="Schedule exception already exists")
    schedules_exception = ExceptionsCrud.update_schedules_exceptions(db, id_schedule_exception, schedules_exception_update)
    return schedules_exception

@schedule_exceptions_router.delete("/{id_schedule_exception}")
async def delete_existing_schedule_exception(id_schedule_exception: int, db: Session = Depends(get_db)):
    schedules_exception = ExceptionsCrud.delete_schedules_exception(db, id_schedule_exception)
    return schedules_exception