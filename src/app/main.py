from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.database import Base, engine
from app.api.v1.router import api_router

API_STR = "/api/v1"

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DBMS Term Project", openapi_url=API_STR + "/openapi.json")
templates = Jinja2Templates(directory="/app/templates")

app.mount("/static", StaticFiles(directory="/app/static"), name="static")
app.include_router(api_router, prefix=API_STR)


@app.get("/")
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get(API_STR + "/")
async def redirection():
    return RedirectResponse(url="/docs")
