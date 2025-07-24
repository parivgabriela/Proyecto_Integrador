import os

MAX_QUESTION_LENGTH = 200  # Limitar el tamaño de la pregunta


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave_default")
    LOG_FILE = "logs/app.log"
    FAQ_FILE = "faq.json"

    @staticmethod
    def init_app(app):
        pass
