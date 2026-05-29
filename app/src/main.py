from flask import Flask
import config
import database
from routes.health import health_bp
from routes.chat import chat_bp
from routes.files import files_bp


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.secret_key = config.FLASK_SECRET_KEY
    app.register_blueprint(health_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(files_bp)
    database.ensure_table()
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
