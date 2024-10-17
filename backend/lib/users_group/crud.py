from sqlalchemy.orm import Session
from models.UsersGroup import UsersGroup
from typing import List

def delete_usergroup_by_user(db: Session, id_user: int):
    db_user_group = db.query(UsersGroup).filter(UsersGroup.id_user == id_user).all()
    for user_group in db_user_group:
        db.delete(user_group)
        db.commit()
        
    return db_user_group

def delete_usergroup_by_group(db: Session, id_group: int):
    db_user_group = db.query(UsersGroup).filter(UsersGroup.id_group == id_group).all()
    for user_group in db_user_group:
        db.delete(user_group)
        
    db.commit()
    
    return db_user_group

def add_user_groups(db: Session, id_user: int, group_ids: List[int]):
    for group_id in group_ids:
        user_group = UsersGroup(id_user=id_user, id_group=group_id)
        db.add(user_group)
    db.commit()