from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.PeopleSchema import PeopleBase, PeopleCreate, PeopleUpdate
from config.database import get_db
from lib.people.crud import get_people, create_people, update_people, delete_people, filter_people, get_person_by_id
from lib.assistance.crud import delete_assistance_by_person, get_yearly_assistance_summary, get_monthly_assistance_summary

people_router = APIRouter(
    prefix="/people",
)

@people_router.get("/", response_model=list[PeopleBase])
async def read_people(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  people = get_people(db, skip=skip, limit=limit)
  return people

@people_router.get("/search")
async def people_filter(q: str, id_user: int = 0, db: Session = Depends(get_db)):
  db_people = filter_people(db, q, id_user)
  return db_people

@people_router.get("/{id_person}", response_model=PeopleBase)
async def get_people_by_id(id_person: int, db: Session = Depends(get_db)):
  return get_person_by_id(db, id_person)

@people_router.post("/", response_model=PeopleBase)
async def create_new_people(people: PeopleCreate, db: Session = Depends(get_db)):
  return create_people(db, people)

@people_router.put("/{id_person}", response_model=PeopleBase)
async def update_existing_people(id_person: int, people_update: PeopleUpdate, db: Session = Depends(get_db)):
  db_people = update_people(db, id_person, people_update)
  return db_people

@people_router.delete("/{id_person}")
async def delete_existing_people(id_person: int, db: Session = Depends(get_db)):
  db_assistance = delete_assistance_by_person(db, id_person)
  db_people = delete_people(db, id_person)
  return db_people

@people_router.get("/{id_person}/assistance/{year}")
async def annual_assistance(id_person: int, year: int, db: Session = Depends(get_db)):
  db_assistance = get_yearly_assistance_summary(db, id_person, year)
  return db_assistance

@people_router.get("/{id_person}/assistance/{year}/{month}")
async def mensual_assistance(id_person: int, year: int, month: str, db: Session = Depends(get_db)):
  db_assistance = get_monthly_assistance_summary(db, id_person, year, month)
  return db_assistance