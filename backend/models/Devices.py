from sqlalchemy import Column, Integer, String
from config.database import Base

class Devices(Base):
  __tablename__ = "devices"

  id_device = Column(Integer, primary_key=True)
  name = Column(String)
  id_config = Column(Integer)
  id_state = Column(Integer)
