from sqlalchemy.orm import Session
from models.Schedules import Schedules

def get_schedule_by_group_and_day(db: Session, id_group: int, day: int):
    return db.query(Schedules).filter(Schedules.id_group == id_group, Schedules.id_day == day).first()

def delete_schedule_by_group(db: Session, id_group: int):
    db.query(Schedules).filter(Schedules.id_group == id_group).delete()
    db.commit()