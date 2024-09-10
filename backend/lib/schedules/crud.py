from sqlalchemy.orm import Session
from models.Schedules import Schedules
from models.Days import Days
from schemas.SchedulesSchema import SchedulesCreate

def get_schedule_by_group_and_day(db: Session, id_group: int, day: int):
    return db.query(Schedules).filter(Schedules.id_group == id_group, Schedules.id_day == day).first()

def get_schedules_by_group(db: Session, id_group: int):
    schedules = db.query(Schedules).filter(Schedules.id_group == id_group).all()
    schedules = [
        {
            "id_schedule": schedule.id_schedule,
            "id_group": schedule.id_group,
            "id_day": schedule.id_day,
            "start_time": str(schedule.start_time),
            "end_time": str(schedule.end_time)
        }
        for schedule in schedules
    ]
    
    return schedules

def get_all_days(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Days).offset(skip).limit(limit).all()

def create_schedules(db: Session, schedules: SchedulesCreate):
    db_schedules = Schedules(
        id_group=schedules.id_group,
        id_day=schedules.id_day,
        start_time=schedules.start_time,
        end_time=schedules.end_time
    )
    db.add(db_schedules)
    db.commit()
    db.refresh(db_schedules)
    return db_schedules