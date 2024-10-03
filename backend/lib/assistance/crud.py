from sqlalchemy.orm import Session
from models.Assistance import Assistance
from models.Periods import Periods
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

def get_periods(db: Session, year: int):
    return db.query(Periods).filter(Periods.year == year).first()

def get_yearly_assistance_summary(db: Session, id_person: int, year: int):
    # Obtener todas las fechas del año específico
    periods = get_periods(db, year)
    start_of_year = periods.start_date
    end_of_year = datetime.today().date()

    if periods.end_date < end_of_year:
        end_of_year = periods.end_date
    
    # Obtener a la persona y su grupo
    person = get_person_by_id(db, id_person)
    
    # Contadores para los resultados
    total_days = 0
    present_count = 0
    late_count = 0
    absent_count = 0

    dates_excluded = []
    dates_included = []

    # Recorrer todos los días del año
    current_date = start_of_year

    while current_date <= end_of_year:
        weekday = current_date.weekday() + 1
        date_str = current_date.strftime("%Y-%m-%d")

        # Obtener el horario y las excepciones para el día actual
        schedule = get_schedule_by_group_and_day(db, person.id_group, weekday)
        schedule_exception = get_schedule_exception_by_group_and_date(db, person.id_group, date_str)

        if not schedule or (schedule_exception and not schedule_exception.is_class) or (current_date >= periods.vacation_start and current_date <= periods.vacation_end):
            # Si no hay clase programada este día, no se cuenta
            current_date += timedelta(days=1)
            dates_excluded.append(date_str)
            continue

        # Incrementar el contador de días de clase
        total_days += 1
        dates_included.append(date_str)

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

def get_monthly_assistance_summary(db: Session, id_person: int, year: int, month: int):
    # Parsear el mes recibido en formato YYYY-MM
    periods = get_periods(db, year)
    start_of_month = datetime.strptime(f"{year}-{month}", "%Y-%m").date()
    end_of_month = (start_of_month.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    
    if (start_of_month < periods.start_date):
        start_of_month = periods.start_date

    if (end_of_month > periods.end_date):
        end_of_month = periods.end_date

    # Obtener a la persona y su grupo
    person = get_person_by_id(db, id_person)
    
    # Lista para almacenar los resultados
    assistance_summary = []

    # Recorrer todos los días del mes
    current_date = start_of_month

    while current_date <= end_of_month:
        weekday = current_date.weekday() + 1
        date_str = current_date.strftime("%Y-%m-%d")

        # Obtener el horario y las excepciones para el día actual
        schedule = get_schedule_by_group_and_day(db, person.id_group, weekday)
        schedule_exception = get_schedule_exception_by_group_and_date(db, person.id_group, date_str)

        if not schedule or (schedule_exception and not schedule_exception.is_class) or (current_date > datetime.today().date()) or (current_date >= periods.vacation_start and current_date <= periods.vacation_end):
            # Si no hay clase programada este día
            assistance_summary.append({
                'date': date_str,
                'assistance': 'no-class'
            })
            current_date += timedelta(days=1)
            continue

        # Determinar la hora de inicio de la clase
        start_time = schedule.start_time
        if schedule_exception:
            start_time = schedule_exception.start_time

        # Obtener la asistencia del día actual
        assistance = db.query(Assistance).filter(Assistance.id_person == id_person, Assistance.date == date_str).first()

        if not assistance:
            # Si no hay registro de asistencia, se cuenta como ausente
            assistance_summary.append({
                'date': date_str,
                'assistance': 'not-assisted'
            })
        else:
            difference = assistance.time - start_time

            if difference > timedelta(minutes=10):
                assistance_summary.append({
                    'date': date_str,
                    'assistance': 'late'
                })
            else:
                assistance_summary.append({
                    'date': date_str,
                    'assistance': 'assisted'
                })

        # Avanzar al siguiente día
        current_date += timedelta(days = 1)
    
    return assistance_summary