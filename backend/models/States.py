from sqlalchemy import Column, Integer, String
from config.database import Base

class States(Base):
  __tablename__ = "states"

  id_state = Column(Integer, primary_key=True)
  state = Column(String)