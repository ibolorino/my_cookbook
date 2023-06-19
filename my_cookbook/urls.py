from fastapi import FastAPI, APIRouter

from my_cookbook.api.v1 import health_router, core_router

from my_cookbook.api.v1.endpoints import users, login, recipes, recipe_items


def configure_routes(app: FastAPI) -> FastAPI:
    v1 = APIRouter(prefix='/api/v1')
    v1.include_router(users.router)
    v1.include_router(login.router)
    v1.include_router(recipes.router)
    v1.include_router(recipe_items.router)

    app.include_router(v1)


    return app
