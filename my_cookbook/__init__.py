import logging
import logging.config

from fastapi import FastAPI

from .urls import configure_routes
from .config import get_settings

logger = logging.getLogger(__name__)
conf = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(title=conf.SERVICE_NAME, debug=conf.DEBUG, version=conf.VERSION)
    app = configure_routes(app=app)

    logging.config.dictConfig(conf.LOGGING)
    logger.info(f'starting app {conf.SERVICE_NAME}')

    return app
