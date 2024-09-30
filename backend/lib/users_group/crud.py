from sqlalchemy.orm import Session
from models.UsersGroup import UsersGroup

def delete_usergroup_by_user(db: Session, id_user: int):
    db_user_group = db.query(UsersGroup).filter(UsersGroup.id_user == id_user).all()
    for user_group in db_user_group:
        db.delete(user_group)
        db.commit()
        
    return db_user_group

