from sqlalchemy.orm import Session
from models.Groups import Groups
from models.People import People
from models.UsersGroup import UsersGroup
from schemas.GroupsSchemas import GroupCreate, GroupUpdate
from lib.assistance.crud import get_today_assistance
from lib.auth.crud import get_user_by_id


def get_groups(db: Session, skip: int = 0, limit: int = 100, id_user: int = 0):
  user = get_user_by_id(db, id_user)

  if id_user == 0 or user is None or (user is not None and user.rol == "admin"):
    return db.query(Groups).offset(skip).limit(limit).all()
  else:
    return db.query(Groups).join(UsersGroup, UsersGroup.id_group == Groups.id_group).filter(UsersGroup.id_user == user.id_user).offset(skip).limit(limit).all()



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
  db_group = Groups(name=group.name,
                    id_device=group.id_device)
  db.add(db_group)
  db.commit()
  db.refresh(db_group)
  return db_group


def update_group(db: Session, id_group: int, group_update: GroupUpdate):
  db_group = db.query(Groups).filter(Groups.id_group == id_group).first()
  if db_group is None:
    return None
  db_group.name = group_update.name
  db_group.id_device = group_update.id_device
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

def update_people_group(db: Session, from_group_id: int, to_group_id: int):
    people_in_group = db.query(People).filter(People.id_group == from_group_id).all()

    for person in people_in_group:
        person.id_group = to_group_id
        db.add(person)
    db.commit()
    return people_in_group