from sqlalchemy import Column, Integer, String, ForeignKey
from config.database import Base

class UsersGroup(Base):
  __tablename__ = "users_group"

  id_user_group = Column(Integer, primary_key=True)
  id_user = Column(Integer, ForeignKey("users.id_user"))
  id_group = Column(Integer, ForeignKey("groups.id_group"))