from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.StatesSchema import StatesBase
from config.database import get_db
from lib.states.crud import get_states

states_router = APIRouter(
    prefix="/states",
)

@states_router.get("/", response_model=List[StatesBase])
async def read_states(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    devices = get_states(db, skip=skip, limit=limit)
    return devices