from sqlalchemy import Column, Integer, String
from config.database import Base

class Periods(Base):
  __tablename__ = "periods"

  id_period = Column(Integer, primary_key=True)
  start_date = Column(String)
  end_date = Column(String)
  vacation_start = Column(String)
  vacation_end = Column(String)
  year = Column(Integer)