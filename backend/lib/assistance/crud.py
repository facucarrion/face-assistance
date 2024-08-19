from sqlalchemy.orm import Session
from models.Assistance import Assistance
from lib.people.crud import get_person_by_id
from lib.schedules.crud import get_schedule_by_group_and_day
from lib.schedule_exceptions.crud import get_schedule_exception_by_group_and_date
from datetime import date as datetimeDate, timedelta

def get_today_assistance(db: Session, id_person: int):
    today = datetimeDate.today()
    person = get_person_by_id(db, id_person)

    weekday = today.weekday() + 1
    date = today.strftime("%Y-%m-%d")

    schedule = get_schedule_by_group_and_day(db, person.id_group, weekday)
    schedule_exception = get_schedule_exception_by_group_and_date(db, person.id_group, date)

    if not schedule or (schedule_exception and schedule_exception.is_class == False):
        return 'no-schedule'

    start_time = schedule.start_time

    if schedule_exception:
        start_time = schedule_exception.start_time

    assistance = db.query(Assistance).filter(Assistance.id_person == id_person, Assistance.date == date).first()

    if not assistance:
        return {'status': 'no-assisted'}

    difference = assistance.time - start_time

    if difference > timedelta(minutes = 10):
        return {
            'status': 'late',
            'time': str(assistance.time)
        }
    
    return {
        'status': 'assisted',
        'time': str(assistance.time)
    }

def delete_assistance_by_person(db: Session, id_person: int):
    db_assistance = db.query(Assistance).filter(Assistance.id_person == id_person).all()
    for assistance in db_assistance:
        db.delete(assistance)
        db.commit()
        
    return db_assistance