from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from config.database import Base

class ScheduleExceptions(Base):
  __tablename__ = "schedule_exceptions"

  id_schedule_exception = Column(Integer, primary_key=True)
  id_group = Column(Integer, ForeignKey("groups.id_group"))
  date = Column(String)
  is_class = Column(Boolean)
  start_time = Column(String)
  end_time = Column(String)