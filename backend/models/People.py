from sqlalchemy import Column, Integer, String, ForeignKey
from config.database import Base

class People(Base):
  __tablename__ = "people"

  id_person = Column(Integer, primary_key=True)
  firstname = Column(String(50))
  lastname = Column(String(50))
  document = Column(String(8))
  image = Column(String(255))
  id_group = Column(Integer, ForeignKey("groups.id_group"))