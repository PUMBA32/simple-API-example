from database import *

from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles


'''
Эта строка, говоря простым языком, создает таблицу в БД для каждой модели, 
унаследовавшей Base. engine содержит настройки подключения, то-есть
мы показываем где именно создавать таблицы, в какой БД 
'''
Base.metadata.create_all(bind=engine)

app = FastAPI()

'''
Эта часть "монтирует" статические файлы (html, css, JS) к приложению.
/static - URL интерфейс по котором будут доступны файлы
StaticFiles указывает, что файлы лежат в директории public
name='static' - внутреннее имя для "монтирования"
'''
app.mount('/static', StaticFiles(directory='public'), name='static')



'''
функция отдает сессию с базой данных эндпоинту, 
дождется пока эндпоинт завершится и закроет db
'''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def main():
    return FileResponse("public/index.html")


@app.get('/api/users')
def get_people(db: Session = Depends(get_db)):  # Depends внедряет механизм зависимостей (Dependency Injection)
    return db.query(Person).all()  # получение всех пользователей из базы данных


@app.get("/api/users/{id}")
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