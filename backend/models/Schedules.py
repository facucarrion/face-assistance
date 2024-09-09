from sqlalchemy import Column, Integer, String, ForeignKey
from config.database import Base

class Schedules(Base):
  __tablename__ = "schedules"

  id_schedule = Column(Integer, primary_key=True)
  id_group = Column(Integer, ForeignKey("groups.id_group"))
  id_day = Column(Integer, ForeignKey("days.id_day"))
  start_time = Column(String(8))
  end_time = Column(String(8))