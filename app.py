from database import *

from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles


# Создание таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount('/static', StaticFiles(directory='public'), name='static')

# определение зависимости
def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()


@app.get('/')
def main():
    return FileResponse("public/index.html")


@app.get('/api/users')
def get_people(db: Session = Depends(get_db)):
    return db.query(Person).all()


@app.get("/api/users/{id}")
def get_person(id, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == id).first()

    if person == None:
        return JSONResponse(
            status_code=404,
            content={
                "message": "user was not found"
            }
        )

    return person


@app.post('/api/users')
def create_person(data = Body(), db: Session = Depends(get_db)):
    person = Person(name=data['name'], age=data['age'])

    db.add(person)
    db.commit()
    db.refresh(person)

    return person


@app.put('/api/users')
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


@app.delete('/api/users/{id}')
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