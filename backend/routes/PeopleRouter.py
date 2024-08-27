from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.PeopleSchema import PeopleBase, PeopleCreate, PeopleUpdate
from config.database import get_db
from lib.people.crud import get_people, create_people, update_people, delete_people, filter_people, get_person_by_id
from lib.assistance.crud import delete_assistance_by_person, get_annual_assistance

people_router = APIRouter(
    prefix="/people",
)

@people_router.get("/", response_model=list[PeopleBase])
async def read_people(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    people = get_people(db, skip = skip, limit = limit)
    return people 

@people_router.get("/search", response_model=list[PeopleBase])
async def people_filter(q: str, db: Session = Depends(get_db)):
    print(f"Query: {q}")
    db_people = filter_people(db, q)
    if not db_people:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
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
    if not db_people:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return db_people

@people_router.delete("/{id_person}")
async def delete_existing_people(id_person: int, db: Session = Depends(get_db)):
    db_assistance = delete_assistance_by_person(db, id_person)
    db_people = delete_people(db, id_person)
    if not db_people:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return db_people

@people_router.get("/{id_person}/assistance")
async def annual_assistance(id_person: int, db: Session = Depends(get_db)):
    db_assistance = get_annual_assistance(db, id_person, year=2024)
    return db_assistance