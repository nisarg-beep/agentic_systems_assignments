from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./studentsdb.db"

engine = create_engine(DATABASE_URL)
