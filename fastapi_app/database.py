import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use environment variable if available, otherwise fallback to default
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://testuser:testpass@postgres/testdb_fastapi")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()