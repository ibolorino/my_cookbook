from fastapi import FastAPI, APIRouter

from my_cookbook.api.v1 import health_router, core_router

from my_cookbook.api.v1.endpoints import users, login


def configure_routes(app: FastAPI) -> FastAPI:
    v1 = APIRouter(prefix='/api/v1')
    v1.include_router(users.router)
    v1.include_router(login.router)

    app.include_router(v1)


    return app
