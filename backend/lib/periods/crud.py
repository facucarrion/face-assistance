from sqlalchemy.orm import Session
from models.Periods import Periods
from datetime import datetime, timedelta
from schemas.PeriodsSchema import PeriodsBase, PeriodsCreate, PeriodsUpdate

def get_periods(db: Session, skip: int = 0, limit: int = 100):
    periods = db.query(Periods).offset(skip).limit(limit).all()

    periods = [
        {
            "id_period": period.id_period,
            "start_date": str(period.start_date),
            "end_date": str(period.end_date),
            "vacation_start": str(period.vacation_start),
            "vacation_end": str(period.vacation_end),
            "year": period.year
        }
        for period in periods
    ]

    return periods

def create_periods(db: Session, periods: PeriodsCreate):
    db_periods = Periods(
        start_date=periods.start_date,
        end_date=periods.end_date,
        vacation_start=periods.vacation_start,
        vacation_end=periods.vacation_end,
        year=periods.year
    )
    db.add(db_periods)
    db.commit()
    db.refresh(db_periods)
    return db_periods

def update_periods(db: Session, id_period: int, periods_update: PeriodsUpdate):
    db_periods = db.query(Periods).filter(Periods.id_period == id_period).first()
    if not db_periods:
        return None
    for key, value in periods_update.dict(exclude_unset=True).items():
        setattr(db_periods, key, value)
    db.commit()
    db.refresh(db_periods)

    db_periods.start_date = str(db_periods.start_date)
    db_periods.end_date = str(db_periods.end_date)
    db_periods.vacation_start = str(db_periods.vacation_start)
    db_periods.vacation_end = str(db_periods.vacation_end)
    db_periods.year = str(db_periods.year)

    return db_periods

def delete_periods(db: Session, id_period: int):
    db_periods = db.query(Periods).filter(Periods.id_period == id_period).first()
    if not db_periods:
        return None
    db.delete(db_periods)
    db.commit()
    return db_periods