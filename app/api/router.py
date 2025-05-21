from fastapi import APIRouter
from .endpoints import auth_requests

api_router = APIRouter()

api_router.include_router(
    auth_requests.router,
    prefix="/auth-requests",
    tags=["authorization-requests"]
) 