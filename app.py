from database import *

from api.schemas import Base
from api.views import router as api_router

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import uvicorn


'''
Эта строка, говоря простым языком, создает таблицу в БД для каждой модели, 
унаследовавшей Base. engine содержит настройки подключения, то-есть
мы показываем где именно создавать таблицы, в какой БД 
'''
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router)

'''
Эта часть "монтирует" статические файлы (html, css, JS) к приложению.
/static - URL интерфейс по котором будут доступны файлы
StaticFiles указывает, что файлы лежат в директории public
name='static' - внутреннее имя для "монтирования"
'''
app.mount('/static', StaticFiles(directory='public'), name='static')


@app.get('/')
def main():
    return FileResponse("public/index.html")


if __name__ == '__main__':
    uvicorn.run('app:app', reload=True)