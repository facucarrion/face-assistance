from sqlalchemy import Column, Integer, String, ForeignKey
from config.database import Base

class Roles(Base):
  __tablename__ = "roles"

  id_rol = Column(Integer, primary_key=True)
  rol = Column(String(9))
  