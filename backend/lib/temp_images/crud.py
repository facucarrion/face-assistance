from sqlalchemy.orm import Session
from models.TempImages import TempImages
from models.Groups import Groups
from models.People import People
from models.Devices import Devices
from lib.people.crud import get_person_by_id
from lib.devices.crud import get_device_by_person

def get_temp_image(db: Session, id_temp_images: int):
    return db.query(TempImages).filter(TempImages.id_temp_images == id_temp_images).first()

def can_upload_temp(db: Session, id_person: int):
    user_temp_images = db.query(TempImages).filter(TempImages.id_person == id_person).all()

    if len(user_temp_images) > 0:
        return False
    
    device = get_device_by_person(db, id_person)

    temp_images = db.query(TempImages).filter(get_device_by_person(db, id_person=TempImages.id_person).id_device == device.id_device).all()

    if len(temp_images) > 0:
        return False

    return True

def create_empty_temp_image(db: Session, id_person: int):
    person = get_person_by_id(db, id_person)

    if can_upload_temp(db, id_person) == False:
        return None
    
    db_temp_image = TempImages(id_person=id_person, image="")
    db.add(db_temp_image)
    db.commit()
    db.refresh(db_temp_image)

    db_device = get_device_by_person(db, id_person)
    db_device.id_state = 2
    db.commit()
    db.refresh(db_device)

    db_temp_image = db.query(TempImages).filter(TempImages.id_temp_images == db_temp_image.id_temp_images).first()
    
    return db_temp_image

def delete_temp_image(db: Session, id_temp_images: int):
    db_temp_image = db.query(TempImages).filter(TempImages.id_temp_images == id_temp_images).first()
    if not db_temp_image:
        return None
    db.delete(db_temp_image)
    db.commit()
    return db_temp_image

def get_temp_image_person_by_device(db: Session, id_config: int):
    db_temp_image = (db
        .query(TempImages)
        .join(People, TempImages.id_person == People.id_person)
        .join(Groups, Groups.id_group == People.id_group)
        .join(Devices, Groups.id_device == Devices.id_device)
        .filter(Devices.id_config == id_config)
        .first()
    )

    return str(db_temp_image.id_person) if db_temp_image else "no temp"