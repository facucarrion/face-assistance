from sqlalchemy import Column, Integer, String, ForeignKey, Time
from config.database import Base

class Assistance(Base):
  __tablename__ = "assistance"

  id_assistance = Column(Integer, primary_key=True)
  id_person = Column(Integer, ForeignKey("people.id_person"))
  date = Column(String(50))
  time = Column(String(8))