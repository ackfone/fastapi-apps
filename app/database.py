from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import setting

# SQLALCHEMY_DATA_URL = "postgresql://postgres:post@localhost:5432/db_fastapi"

#create and set databse info in .env in root folder
SQLALCHEMY_DATA_URL = f"postgresql://{setting.db_username}:{setting.db_password}@{setting.db_host}:{setting.db_port}/{setting.db_name}"

Engine = create_engine(SQLALCHEMY_DATA_URL)

SessionLocal = sessionmaker(bind=Engine, autocommit=False, autoflush=False)

Base = declarative_base()

#dependecy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


