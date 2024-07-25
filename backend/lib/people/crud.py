from sqlalchemy.orm import Session
from models.People import People
from schemas.PeopleSchema import PeopleCreate, PeopleUpdate

def get_people(db: Session, skip: int = 0, limit: int = 100):
    return db.query(People).offset(skip).limit(limit).all()

def create_people(db: Session, people: PeopleCreate):
    db_people = People(
        firstname=people.firstname,
        lastname=people.lastname,
        document=people.document,
        image=people.image,
        id_group=people.id_group
    )
    db.add(db_people)
    db.commit()
    db.refresh(db_people)
    return db_people

def update_people(db: Session, id_person: int, people_update: PeopleUpdate):
    db_people = db.query(People).filter(People.id_person == id_person).first()
    if not db_people:
        return None
    for key, value in people_update.dict(exclude_unset=True).items():
        setattr(db_people, key, value)
    db.commit()
    db.refresh(db_people)
    return db_people

def delete_people(db: Session, id_person: int):
    db_people = db.query(People).filter(People.id_person == id_person).first()
    if not db_people:
        return None
    db.delete(db_people)
    db.commit()
    return db_people