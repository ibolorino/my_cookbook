from fastapi import APIRouter
from pydantic import BaseModel

from my_cookbook.config import get_settings

settings = get_settings()

health_router = APIRouter()


class Health(BaseModel):
    version: str = "v1"
    status: str = "running"


@health_router.get("/health", tags=["health"], response_model=Health)
async def healthcheck():
    return Health()
