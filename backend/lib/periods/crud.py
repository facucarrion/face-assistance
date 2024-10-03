from sqlalchemy.orm import Session
from models.Periods import Periods
from datetime import datetime, timedelta
from schemas.PeriodsSchema import PeriodsBase, PeriodsCreate, PeriodsUpdate

def create_periods(db: Session, periods: PeriodsCreate):
    db_periods = Periods(
        id_period=periods.id_period,
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

