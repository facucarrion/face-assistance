from sqlalchemy.orm import Session
from models.Schedules import Schedules
from models.Groups import Groups
from models.Days import Days
from schemas.SchedulesSchema import SchedulesCreate, SchedulesUpdate

def get_schedules_by_group(db: Session, id_group: int):
  db_schedule = (db
    .query(Schedules, Days.day)
    .join(Groups, Schedules.id_group == Groups.id_group)
    .join(Days, Schedules.id_day == Days.id_day)
    .filter(Schedules.id_group == id_group)
    .all()
  )

  schedule = [
    {
      'id_schedule': schedule.id_schedule,
      'id_group': schedule.id_group,
      'id_day': schedule.id_day,
      'start_time': str(schedule.start_time),
      'end_time': str(schedule.end_time),
      'day': day
    }
    for schedule, day in db_schedule
  ]  

  return schedule

def get_schedule_by_group_and_day(db: Session, id_group: int, day: int):
    return db.query(Schedules).filter(Schedules.id_group == id_group, Schedules.id_day == day).first()

def delete_schedule_by_group(db: Session, id_group: int):
    db.query(Schedules).filter(Schedules.id_group == id_group).delete()
    db.commit()
    
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

def delete_schedules(db: Session, id_schedule: int):
    db_schedules = db.query(Schedules).filter(Schedules.id_schedule == id_schedule).first()
    if not db_schedules:
        return None
    db.delete(db_schedules)
    db.commit()
    return db_schedules

def update_schedules(db: Session, id_schedule: int, schedules_update: SchedulesUpdate):
    db_schedules = db.query(Schedules).filter(Schedules.id_schedule == id_schedule).first()
    if not db_schedules:
        return None
    for key, value in schedules_update.dict(exclude_unset=True).items():
        setattr(db_schedules, key, value)
    db.commit()
    db.refresh(db_schedules)
    db_schedules.start_time = str(db_schedules.start_time)
    db_schedules.end_time = str(db_schedules.end_time)

    return db_schedules
