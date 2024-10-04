from sqlalchemy import Column, Integer, String
from config.database import Base

class TempImages(Base):
  __tablename__ = "temp_images"

  id_temp_images = Column(Integer, primary_key=True)
  id_person = Column(Integer)
  image = Column(String)