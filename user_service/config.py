from decouple import config
from datetime import timedelta


class Config:
    SECRET_KEY = config("USER_SERVICE_SECRET_KEY")
    JSON_SORT_KEYS = False

    JWT_SECRET_KEY = config("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(config("JWT_ACCESS_TOKEN_EXPIRES", default=3600))
    )

    SWAGGER = {"title": "User Service API", "uiversion": 3}


import os

SWAGGER_DOCS_PATH = os.path.join(os.path.dirname(__file__), "swagger_docs")
