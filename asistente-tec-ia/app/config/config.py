import os

MAX_QUESTION_LENGTH = 200  # Limitar el tamaño de la pregunta


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave_default")
    LOG_FILE = "logs/app.log"
    FAQ_FILE = "faq.json"

    @staticmethod
    def init_app(app):
        import logging
        from logging.handlers import RotatingFileHandler

        file_handler = RotatingFileHandler(Config.LOG_FILE, maxBytes=100000, backupCount=3)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        app.logger.addHandler(file_handler)
