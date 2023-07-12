from fastapi import FastAPI, APIRouter

from my_cookbook.api.v1.endpoints import step, login, users, recipes, ingredient, recipe_items


def configure_routes(app: FastAPI) -> FastAPI:
    v1 = APIRouter(prefix="/api/v1")
    v1.include_router(login.router, tags=["Auth"])
    v1.include_router(ingredient.router, tags=["Ingredients"])
    v1.include_router(recipes.router, tags=["Recipes"])
    v1.include_router(recipe_items.router, tags=["Recipe Items"])
    v1.include_router(step.router, tags=["Steps"])
    v1.include_router(users.router, tags=["Usuários"])

    app.include_router(v1)

    return app
