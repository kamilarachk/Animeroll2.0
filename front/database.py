from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./animeroll.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}, 
    echo=True
)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)