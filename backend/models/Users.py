from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class User(Base):
  __tablename__ = "users"

  id_user = Column(Integer, primary_key=True)
  username = Column(String(20), unique=True)
  password = Column(String(60))
  id_rol = Column(Integer, ForeignKey("roles.id_rol"), default = 2)
  rol = relationship("Roles", back_populates="users")

class Roles(Base):
  __tablename__ = "roles"

  id_rol = Column(Integer, primary_key=True)
  rol = Column(String(20))
  users = relationship("User", back_populates="rol")