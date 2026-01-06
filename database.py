from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Column, Integer, String


SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_app.db'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={
        "check_same_thread": False
    }
)


class Base(DeclarativeBase): pass 
class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer,)


SessionLocal = sessionmaker(autoflush=False, bind=engine)
