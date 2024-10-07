from sqlalchemy import Column, Integer, String, ForeignKey
from config.database import Base

class Groups(Base):
  __tablename__ = "groups"

  id_group = Column(Integer, primary_key=True)
  name = Column(String(40))
  id_device = Column(Integer, ForeignKey("devices.id_device"))