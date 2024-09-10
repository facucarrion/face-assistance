from sqlalchemy.orm import Session
from models.ScheduleExceptions import ScheduleExceptions
from schemas.SchedulesExceptionsSchema import SchedulesExceptionsBase, ExceptionsCreate

def create_exceptions(db: Session, schedules_exceptions: ExceptionsCreate):
    db_schedules_exceptions = ScheduleExceptions(
        id_group=schedules_exceptions.id_group,
        date=schedules_exceptions.date,
        is_class=schedules_exceptions.is_class,
        start_time=schedules_exceptions.start_time,
        end_time=schedules_exceptions.end_time
    )
    db.add(db_schedules_exceptions)
    db.commit()
    db.refresh(db_schedules_exceptions)
    return db_schedules_exceptions

def get_schedule_exception_by_group_and_date(db: Session, id_group: int, date: str):
    return db.query(ScheduleExceptions).filter(ScheduleExceptions.id_group == id_group, ScheduleExceptions.date == date).first()

def delete_schedule_exception_by_group(db: Session, id_group: int):
    db.query(ScheduleExceptions).filter(ScheduleExceptions.id_group == id_group).delete()
    db.commit()