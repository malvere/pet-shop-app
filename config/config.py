from dataclasses import dataclass
import logging
from os import getenv


@dataclass
class Server:
    web_app_host: str = getenv("HOST", "localhost")
    web_app_port: int = int(getenv("PORT", "8000"))


@dataclass
class JWT:
    secret_key: str = getenv("JWT_SECRET_KEY", "secret")
    algorithm: str = getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


@dataclass
class DataBase:
    url: str = getenv("DB_URL", "sqlite:///:memory:")


@dataclass
class Config:
    logging_level: int = int(getenv("LOGGING_LEVEL", logging.DEBUG))
    server = Server()
    jwt = JWT()
    db = DataBase()


conf = Config()
