from os import environ
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

user = environ["POSTGRES_USER"]
password = environ["POSTGRES_PASSWORD"]
host = environ["POSTGRES_HOST"]
dbname = environ["POSTGRES_DB"]

connection_string = f"postgresql://{user}:{password}@{host}/{dbname}"
engine = create_engine(connection_string, pool_pre_ping=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Session: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
