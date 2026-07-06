from flask import Flask
from flask_cors import CORS

from config import Config
from database import db, migrate

from models import Contract

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/")
    def health():

        return {
            "status": "Athena Backend Running"
        }

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)