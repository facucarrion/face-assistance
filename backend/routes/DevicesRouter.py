from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.DevicesSchema import DevicesBase, DevicesCreate, DevicesUpdate
from config.database import get_db
from lib.devices.crud import get_devices, get_device_by_id, create_device, update_device, delete_devices

devices_router = APIRouter(
    prefix="/devices",
)

@devices_router.get("/", response_model=List[DevicesBase])
async def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    devices = get_devices(db, skip=skip, limit=limit)
    return devices

@devices_router.get("/{id_device}", response_model=DevicesBase)
async def get_device_by_id(id_device: int, db: Session = Depends(get_db)):
    return get_device_by_id(db, id_device)

@devices_router.post("/")
async def create_new_device(device: DevicesCreate, db: Session = Depends(get_db)):
    return create_device(db, device)

@devices_router.put("/{id_device}")
async def update_devices(id_device: int, device_update: DevicesUpdate, db: Session = Depends(get_db)):
    devices = update_device(db, id_device, device_update)
    return devices

@devices_router.delete("/{id_device}")
async def delete_device(id_device: int, db: Session = Depends(get_db)):
    devices = delete_devices(db, id_device)
    return devices