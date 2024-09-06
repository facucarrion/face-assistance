from sqlalchemy.orm import Session
from models.ScheduleExceptions import ScheduleExceptions

def get_schedule_exception_by_group_and_date(db: Session, id_group: int, date: str):
    return db.query(ScheduleExceptions).filter(ScheduleExceptions.id_group == id_group, ScheduleExceptions.date == date).first()

def delete_schedule_exception_by_group(db: Session, id_group: int):
    db.query(ScheduleExceptions).filter(ScheduleExceptions.id_group == id_group).delete()
    db.commit()