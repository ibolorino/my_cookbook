import logging
import logging.config

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .config import get_settings
from .urls import configure_routes

logger = logging.getLogger(__name__)
conf = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title=conf.SERVICE_NAME,
        debug=conf.DEBUG,
        version=conf.VERSION,
        openapi_url="/openapi.json",
    )

    if conf.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in conf.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app = configure_routes(app=app)

    logging.config.dictConfig(conf.LOGGING)
    logger.info(f"starting app {conf.SERVICE_NAME}")

    return app
