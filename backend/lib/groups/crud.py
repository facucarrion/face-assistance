from sqlalchemy.orm import Session
from models.Groups import Groups
from models.People import People
from schemas.GroupsSchemas import GroupCreate, GroupUpdate
from lib.assistance.crud import get_today_assistance

def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Groups).offset(skip).limit(limit).all()

def get_group_by_id(db: Session, id_group: int = 0):
    return db.query(Groups).filter(Groups.id_group == id_group).first()
    

def get_group_with_people_by_id(db: Session, id_group: int = 0):
    groups = db.query(Groups).filter(Groups.id_group == id_group).first()
    people = db.query(People).filter(People.id_group == id_group).all()

    people = [
        {
            "id_person": person.id_person,
            "firstname": person.firstname,
            "lastname": person.lastname,
            "document": person.document,
            "image": person.image,
            "id_group": person.id_group,
            "assistance": get_today_assistance(db, person.id_person)

        }
        for person in people
    ]

    return {
        "id_group": groups.id_group,
        "name": groups.name,
        "people": people
    }

def create_group(db: Session, group: GroupCreate):
    db_group = Groups(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def update_group(db: Session, id_group: int, group_update: GroupUpdate):
    db_group = db.query(Groups).filter(Groups.id_group == id_group).first()
    if db_group is None:
        return None
    db_group.name = group_update.name
    db.commit()
    db.refresh(db_group)
    return db_group

def delete_group(db: Session, id_group: int):
    db_group = db.query(Groups).filter(Groups.id_group == id_group).first()
    if db_group is None:
        return None
    db.delete(db_group)
    db.commit()
    return db_group

def get_people_in_group(db: Session, id_group: int):
    return db.query(People).filter(People.id_group == id_group).all()