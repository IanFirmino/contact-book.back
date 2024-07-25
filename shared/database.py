from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

password = "1q2w3e4r@#$"
password_encoded = quote_plus(password)
SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc://sa:{password_encoded}@127.0.0.1,1433/fast_api_zero_to_deploy?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()