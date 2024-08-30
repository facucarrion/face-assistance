from sqlalchemy.orm import Session
from models.Assistance import Assistance
from lib.people.crud import get_person_by_id
from lib.schedules.crud import get_schedule_by_group_and_day
from lib.schedule_exceptions.crud import get_schedule_exception_by_group_and_date
from datetime import date as datetimeDate, timedelta, datetime

def get_today_assistance(db: Session, id_person: int):
    today = datetimeDate.today()
    person = get_person_by_id(db, id_person)

    weekday = today.weekday() + 1
    date = today.strftime("%Y-%m-%d")

    schedule = get_schedule_by_group_and_day(db, person.id_group, weekday)
    schedule_exception = get_schedule_exception_by_group_and_date(db, person.id_group, date)

    if not schedule or (schedule_exception and schedule_exception.is_class == False):
        return {
            'status': 'no-schedule'
        }

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

def get_yearly_assistance_summary(db: Session, id_person: int, year: int):
    # Obtener todas las fechas del año específico
    start_of_year = datetime(year, 1, 1).date()
    end_of_year = datetime.today().date()
    
    # Obtener a la persona y su grupo
    person = get_person_by_id(db, id_person)
    
    # Contadores para los resultados
    total_days = 0
    present_count = 0
    late_count = 0
    absent_count = 0

    # Recorrer todos los días del año
    current_date = start_of_year

    while current_date <= end_of_year:
        weekday = current_date.weekday() + 1
        date_str = current_date.strftime("%Y-%m-%d")

        # Obtener el horario y las excepciones para el día actual
        schedule = get_schedule_by_group_and_day(db, person.id_group, weekday)
        schedule_exception = get_schedule_exception_by_group_and_date(db, person.id_group, date_str)

        if not schedule or (schedule_exception and not schedule_exception.is_class):
            # Si no hay clase programada este día, no se cuenta
            current_date += timedelta(days=1)
            continue

        # Incrementar el contador de días de clase
        total_days += 1

        # Determinar la hora de inicio de la clase
        start_time = schedule.start_time
        if schedule_exception:
            start_time = schedule_exception.start_time

        # Obtener la asistencia del día actual
        assistance = db.query(Assistance).filter(Assistance.id_person == id_person, Assistance.date == date_str).first()

        if not assistance:
            # Si no hay registro de asistencia, se cuenta como ausente
            absent_count += 1
        else:
            difference = assistance.time - start_time

            if difference > timedelta(minutes=10):
                late_count += 1
            else:
                present_count += 1

        # Avanzar al siguiente día
        current_date += timedelta(days=1)
    
    # Retornar los resultados
    return {
        'total_days': total_days,
        'assisted': present_count,
        'late': late_count,
        'not-assisted': absent_count
    }