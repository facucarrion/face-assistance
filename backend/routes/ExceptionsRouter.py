from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.SchedulesExceptionsSchema import SchedulesExceptionsBase, ExceptionsCreate
from config.database import get_db
from lib.schedule_exceptions.crud import create_exceptions

schedule_exceptions_router = APIRouter(
    prefix="/schedule_exceptions",
)

@schedule_exceptions_router.post("/")
async def create_new_exceptions(schedules_excetions: ExceptionsCreate, db: Session = Depends(get_db)):
    return create_exceptions(db, schedules_excetions)