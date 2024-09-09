from sqlalchemy import Column, Integer, String, ForeignKey
from config.database import Base

class Days(Base):
  __tablename__ = "days"

  id_day = Column(Integer, primary_key=True)
  day = Column(String, index=True)