from sqlalchemy.orm import Session
from models.Devices import Devices
from models.States import States
from schemas.DevicesSchema import DevicesBase, DevicesCreate, DevicesUpdate

def get_devices(db: Session, skip: int = 0, limit: int = 100):
  devices = db.query(Devices, States.state).join(States, Devices.id_state == States.id_state).offset(skip).limit(limit).all()
  
  devices = [
    {
      "id_device": device.id_device,
      "name": device.name,
      "id_config": device.id_config,
      "id_state": device.id_state,
      "state": state
    }
    for [device, state] in devices
  ]

  return devices

def get_device_by_id(db: Session, id_device: int = 0):
  device = db.query(Devices, States.state).join(States, Devices.id_state == States.id_state).filter(Devices.id_device == id_device).first()

  [device, state] = device

  return {
    "id_device": device.id_device,
    "name": device.name,
    "id_config": device.id_config,
    "state": state
  }

def create_device(db: Session, device):
  db_device = Devices(name=device.name, id_state=device.id_state, id_config=device.id_config)
  db.add(db_device)
  db.commit()
  db.refresh(db_device)
  return db_device

def update_device(db: Session, id_device: int, device_update: DevicesUpdate):
    db_device = db.query(Devices).filter(Devices.id_device == id_device).first()
    if not db_device:
        return None
    for key, value in device_update.dict(exclude_unset=True).items():
        setattr(db_device, key, value)
    db.commit()
    db.refresh(db_device)

    return db_device

def delete_devices(db: Session, id_device: int):
    db_device = db.query(Devices).filter(Devices.id_device == id_device).first()
    if not db_device:
        return None
    db.delete(db_device)
    db.commit()
    return db_device