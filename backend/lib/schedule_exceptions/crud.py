from sqlalchemy.orm import Session
from models.ScheduleExceptions import ScheduleExceptions
from schemas.SchedulesExceptionsSchema import SchedulesExceptionsBase, ExceptionsCreate, ExceptionsUpdate
from datetime import datetime, timedelta

def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

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
            "start_time": format_timedelta(exception.start_time),
            "end_time": format_timedelta(exception.end_time),
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
    db_schedules_exceptions = db.query(ScheduleExceptions).filter(ScheduleExceptions.id_schedule_exception == id_schedule_exception).first()
    if not db_schedules_exceptions:
        return None
    for key, value in schedules_exception_update.dict(exclude_unset=True).items():
        setattr(db_schedules_exceptions, key, value)
    db.commit()
    db.refresh(db_schedules_exceptions)

    db_schedules_exceptions.date = str(db_schedules_exceptions.date)
    db_schedules_exceptions.is_class = bool(db_schedules_exceptions.is_class)
    db_schedules_exceptions.start_time = str(db_schedules_exceptions.start_time)
    db_schedules_exceptions.end_time = str(db_schedules_exceptions.end_time)

    return db_schedules_exceptions

def delete_schedules_exception(db: Session, id_schedule_exception: int):
    db_schedules_exception = db.query(ScheduleExceptions).filter(ScheduleExceptions.id_schedule_exception == id_schedule_exception).first()
    if not db_schedules_exception:
        return None
    db.delete(db_schedules_exception)
    db.commit()
    return db_schedules_exception