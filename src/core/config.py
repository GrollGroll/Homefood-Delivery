import os
from logging import config as logging_config

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

from .logger import LOGGING

logging_config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    database_dsn: PostgresDsn
    project_name: str
    project_host: str
    project_port: int
    bot_token: str

    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        env_file = '.env'


app_settings = AppSettings()
