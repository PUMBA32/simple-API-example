import uuid

from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse, FileResponse

from typing import Optional


class Person:
    def __init__(self, name: str, age: int):
        self.name: str = name
        self.age: int = age
        self.id = str(uuid.uuid4())


# условная база данных 
people = [Person('Tyler', 23), Person('Edvard', 20), Person('Mike', 34)]


def find_person(id: int) -> Optional[Person]:
    for person in people:
        if person.id == id:
            return person
    return 


app = FastAPI()


@app.get('/')
async def main():
    return FileResponse("public/index.html")


@app.get('/api/users')
def get_people():
    return people


@app.get('/api/users/{id}')
def get_person(id: int):
    person = find_person(id)
    print(person)

    if person == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": 'Пользователь не найден'}
        )

    return person


@app.post('/api/users')
def create_person(data = Body()):
    person = Person(data['name', data['age']])
    people.append(person)
   
    return person


@app.put('/api/users')
def edit_person(data = Body()):
    person = find_person(data['id'])

    if person == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Пользователь не найден"}
        )
    
    person.age = data['age']
    person.name = data['name']
   
    return person


@app.delete('/api/users/{id}')
def delete_person(id: int):
    person = find_person(id)

    if person == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Пользователь не найден"}
        )
    
    people.remove(person)
    return person



