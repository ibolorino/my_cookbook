import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)


core_router = APIRouter()

@core_router.get('/teste', tags=['teste'])
def teste():
    return {"OK": "OK"}