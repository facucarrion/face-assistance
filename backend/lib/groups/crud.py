from sqlalchemy.orm import Session

from models.Groups import Groups

def get_group(db: Session, skip: int = 0, limit: int = 100):
  groups = (db
    .query(Groups.id_group, Groups.name)
    .offset(skip)
    .limit(limit)
    .all()
  )
  
  return groups