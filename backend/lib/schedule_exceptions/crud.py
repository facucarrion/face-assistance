from sqlalchemy.orm import Session
from models.ScheduleExceptions import ScheduleExceptions
from schemas.SchedulesExceptionsSchema import SchedulesExceptionsBase, ExceptionsCreate, ExceptionsUpdate
from datetime import datetime, timedelta

def get_schedule_exceptions_by_group(db: Session, id_group: int):
    # Obtener la fecha actual
    today = datetime.today()

    # Calcular la fecha límite de los próximos 30 días
    thirty_days_from_now = today + timedelta(days=30)

    # Filtrar por grupo y excepciones dentro de los próximos 30 días
    exceptions = db.query(ScheduleExceptions).filter(
        ScheduleExceptions.id_group == id_group,
        ScheduleExceptions.date >= today,
        ScheduleExceptions.date <= thirty_days_from_now
    ).all()

    exceptions = [
        {
            "id_schedule_exception": exception.id_schedule_exception,
            "id_group": exception.id_group,
            "start_time": str(exception.start_time),
            "end_time": str(exception.end_time),
            "is_class": exception.is_class,
            "date": exception.date
        }
        for exception in exceptions
    ]

    return exceptions

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

def update_schedules_exceptions(db: Session, id_schedule_exception: int, schedules_exception_update: ExceptionsUpdate):
    db_schedules_exception = db.query(ScheduleExceptions).filter(ScheduleExceptions.id_schedule_exception == id_schedule_exception).first()
    if not db_schedules_exception:
        return None
    for key, value in schedules_exception_update.dict(exclude_unset=True).items():
        setattr(db_schedules_exception, key, value)
    db.commit()
    db.refresh(db_schedules_exception)
    db_schedules_exception.date = str(db_schedules_exception.date)
    db_schedules_exception.is_class = bool(db_schedules_exception.is_class)
    db_schedules_exception.start_time = str(db_schedules_exception.start_time)
    db_schedules_exception.end_time = str(db_schedules_exception.end_time)

    return db_schedules_exception