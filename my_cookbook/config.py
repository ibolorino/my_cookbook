from typing import Optional, Dict, Any
from functools import lru_cache

from pydantic import BaseSettings, validator, PostgresDsn


class Settings(BaseSettings):
    ENVIRONMENT: str = ''
    SERVICE_NAME: str = 'my_cookbook'
    VERSION: str = '1.0.0'
    DEBUG: bool = False
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    DATABASE_URI: Optional[PostgresDsn] = None

    LOG_LEVEL: str = 'INFO'

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '[%(asctime)s][%(levelname)s] %(name)s '
                '%(filename)s:%(funcName)s:%(lineno)d | %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
        },
        'handlers': {
            'default': {
                'level': LOG_LEVEL,
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout'
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': LOG_LEVEL,
                'propagate': False
            },
        },
    }

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # JWT

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SECRET_KEY: str = "X*$DqrzZ1Hk%V8CeN%yVhsojXl999JAENuohPsz1Ncx%Qe6sp@"
    JWT_ALGORITHM: str = "HS256"


    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
