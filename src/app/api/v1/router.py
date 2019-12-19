from fastapi import APIRouter
from app.api.v1.endpoints import users, hospitals, shops, prescriptions, drugs, login

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(hospitals.router, prefix="/hospitals", tags=["hospitals"])
api_router.include_router(shops.router, prefix="/shops", tags=["shops"])
api_router.include_router(
    prescriptions.router, prefix="/prescriptions", tags=["prescriptions"]
)
api_router.include_router(drugs.router, prefix="/drugs", tags=["drugs"])
api_router.include_router(login.router, tags=["login"])
