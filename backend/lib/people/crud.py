from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.People import People
from models.Assistance import Assistance
from schemas.PeopleSchema import PeopleCreate, PeopleUpdate


def get_people(db: Session, skip: int = 0, limit: int = 100):
    return db.query(People).offset(skip).limit(limit).all()

def get_person_by_id(db: Session, id_person: int):
    return db.query(People).filter(People.id_person == id_person).first()

def get_annual_assistance(db: Session, id_person: int, year: int):
    return db.query(Assistance).filter(
        Assistance.id_person == id_person,
        Assistance.date >= f"{year}-01-01",
        Assistance.date <= f"{year}-12-31"
    ).all()

def create_people(db: Session, people: PeopleCreate):
    db_people = People(
        firstname=people.firstname,
        lastname=people.lastname,
        document=people.document,
        email=people.email,
        phone_number=people.phone_number,
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

def delete_people_by_group(db: Session, id_group: int):
    db_people = db.query(People).filter(People.id_group == id_group).all()
    for person in db_people:
        db.delete(person)
    db.commit()
    return db_people

def filter_people(db: Session, q: str):
    db_people = db.query(People).filter(
        or_(
            People.firstname.like(f"%{q}%"),
            People.lastname.like(f"%{q}%"),
            People.document.like(f"%{q}%")
        )
    ).all()
    return db_people