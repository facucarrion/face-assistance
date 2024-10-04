from sqlalchemy.orm import Session
from models.TempImages import TempImages

def create_empty_temp_image(db: Session, id_person: int):
    db_temp_image = TempImages(id_person=id_person, image="")
    db.add(db_temp_image)
    db.commit()
    db.refresh(db_temp_image)

    db_temp_image = db.query(TempImages).filter(TempImages.id_temp_images == db_temp_image.id_temp_images).first()
    
    return db_temp_image

def delete_temp_image(db: Session, id_temp_images: int):
    db_temp_image = db.query(TempImages).filter(TempImages.id_temp_images == id_temp_images).first()
    if not db_temp_image:
        return None
    db.delete(db_temp_image)
    db.commit()
    return db_temp_image