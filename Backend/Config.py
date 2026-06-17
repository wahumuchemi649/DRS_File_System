
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "DRS_File_System")




DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# The engine acts as the core interface to the database
engine = create_engine(DATABASE_URL, echo=False)

# SessionLocal is a class factory for database session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# The base class that maps our Python classes directly to database tables
Base = declarative_base()
