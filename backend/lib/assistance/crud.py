from sqlalchemy.orm import Session
from models.Assistance import Assistance

def delete_assistance_by_person(db: Session, id_person: int):
    db_assistance = db.query(Assistance).filter(Assistance.id_person == id_person).all()
    for assistance in db_assistance:
        db.delete(assistance)
        db.commit()
        
    return db_assistance