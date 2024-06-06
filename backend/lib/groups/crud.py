from sqlalchemy.orm import Session

from models.Groups import Groups
from schemas.GroupsSchemas import GroupCreate

def get_group(db: Session, skip: int = 0, limit: int = 100):
  groups = (db
    .query(Groups.id_group, Groups.name)
    .offset(skip)
    .limit(limit)
    .all()
  )
  
  return groups

def create_group(db: Session, group: GroupCreate):
    db_group = Groups(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group
