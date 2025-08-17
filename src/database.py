from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings
 
engine = create_engine(settings.get_database_url(), pool_recycle=7200)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        print("Entra al finally del generador get_db")
        db.close()
