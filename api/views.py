from database import *

from api.crud import get_db
from api.schemas import Person

from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session


router = APIRouter()


@router.get('/api/users')
def get_people(db: Session = Depends(get_db)):  # Depends внедряет механизм зависимостей (Dependency Injection)
    return db.query(Person).all()  # получение всех пользователей из базы данных


@router.get("/api/users/{id}")
def get_person(id, db: Session = Depends(get_db)):
    # получение конкретного пользователя по его id
    person = db.query(Person).filter(Person.id == id).first()

    if person == None:
        return JSONResponse(
            status_code=404,
            content={
                "message": "user was not found"
            }
        )

    return person


@router.post('/api/users')
def create_person(data = Body(), db: Session = Depends(get_db)):
    person = Person(name=data['name'], age=data['age'])

    db.add(person)
    db.commit()
    db.refresh(person)

    return person


@router.put('/api/users')
def edit_person(data = Body(), db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == data['id']).first()

    if person == None:
        return JSONResponse(
            status_code=404,
            content={
                "message": "user was not found"
            }
        )

    person.age = data['age']
    person.name = data['name']

    db.commit()
    db.refresh(person)

    return person


@router.delete('/api/users/{id}')
def delete_person(id, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == id).first()

    if person == None:
        return JSONResponse(
            status_code=404,
            content={
                "message": "user was not found"
            }
        )
    
    db.delete(person)
    db.commit()

    return person