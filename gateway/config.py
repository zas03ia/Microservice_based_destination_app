from decouple import config


class Config:
    SECRET_KEY = config("GATEWAY_SECRET_KEY")
    DEBUG = config("DEBUG", cast=bool, default=False)
    DESTINATION_SERVICE_URL = config("DESTINATION_SERVICE_URL")
    USER_SERVICE_URL = config("USER_SERVICE_URL")
    AUTH_SERVICE_URL = config("AUTH_SERVICE_URL")
    SWAGGER = {"title": "Travel API Gateway", "uiversion": 3}
