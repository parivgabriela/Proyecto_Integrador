from flask import Flask
from routes.tec_ia_rutas import tec_ia_bot
from config.config import Config, socketio
from config.logging_config import setup_logging
from services.constants_process import UPLOAD_FOLDER

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ---
socketio.init_app(app)

setup_logging()

app.register_blueprint(tec_ia_bot)

if __name__ == "__main__":
    app.run(debug=True)

