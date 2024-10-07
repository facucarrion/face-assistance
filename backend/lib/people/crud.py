from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.People import People
from models.Groups import Groups
from models.Assistance import Assistance
from models.UsersGroup import UsersGroup
from models.Devices import Devices
from schemas.PeopleSchema import PeopleCreate, PeopleUpdate
from lib.auth.crud import get_user_by_id


def get_people(db: Session, skip: int = 0, limit: int = 100):
    db_people = (
        db.query(People, Groups, Devices)
        .join(Groups, Groups.id_group == People.id_group).join(Devices, Groups.id_device == Devices.id_device, isouter=True)
        .order_by(People.id_group)
        .offset(skip).limit(limit).all()
    )

    db_people = [
        {
            'id_person': person.id_person,
            'firstname': person.firstname,
            'lastname': person.lastname,
            'document': person.document,
            'email': person.email,
            'phone_number': person.phone_number,
            'id_group': person.id_group,
            'group_name': group.name,
            'device_name': device.name if device else None
        }
        for person, group, device in db_people
    ]

    return db_people

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
    db_people = db.query(People).filter(People.id_group == id_group).delete()
    db.commit()
    return db_people

def filter_people(db: Session, q: str, id_user: int):
    user = get_user_by_id(db, id_user)
    filtered_people = []

    if id_user == 0 or user is None or (user is not None and user.rol == "admin"):
        filtered_people = db.query(People, Groups.name).join(Groups, People.id_group == Groups.id_group).filter(
        (People.firstname.like(f"%{q}%")) |
        (People.lastname.like(f"%{q}%")) |
        (People.document.like(f"%{q}%"))
    ).all()

    else:
        filtered_people = db.query(People, Groups.name).join(Groups, People.id_group == Groups.id_group).join(UsersGroup, UsersGroup.id_group == Groups.id_group).filter(
        ((People.firstname.like(f"%{q}%")) |
        (People.lastname.like(f"%{q}%")) |
        (People.document.like(f"%{q}%")))).filter(UsersGroup.id_user == user.id_user).all()

    # Convertir los resultados en una lista de diccionarios
    result = [
        {
            'id_person': person.id_person,
            'firstname': person.firstname,
            'lastname': person.lastname,
            'document': person.document,
            'id_group': person.id_group,
            'group_name': group_name
        }
        for person, group_name in filtered_people
    ]

    return result