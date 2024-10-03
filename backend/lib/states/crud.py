from sqlalchemy.orm import Session
from models.States import States

def get_states(db: Session, skip: int = 0, limit: int = 100):
  return db.query(States).offset(skip).limit(limit).all()