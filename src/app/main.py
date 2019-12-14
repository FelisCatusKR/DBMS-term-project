from fastapi import FastAPI

from app.database import Base, engine
from app.api.v1.router import api_router

API_STR = "/api/v1"

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DBMS Term Project", openapi_url=API_STR + "/openapi.json")
app.include_router(api_router, prefix=API_STR)
