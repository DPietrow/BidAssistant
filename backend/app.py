from flask import Flask
from flask_cors import CORS

from config import Config
from database import db, migrate

# Import models so Flask-Migrate discovers them
from models import Contract

# Register routes
from routes.contracts import contracts_bp
from routes.ingestion import ingestion_bp
from routes.search import search_bp
from routes.embeddings import embedding_bp
from routes.ask import ask_bp
from routes.athena import athena_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(contracts_bp)
    app.register_blueprint(ingestion_bp)
    app.register_blueprint(
        search_bp,
        url_prefix="/api/search"
    )   
    app.register_blueprint(embedding_bp)
    app.register_blueprint(ask_bp)
    app.register_blueprint(athena_bp)


    @app.route("/")
    def root():

        return {
            "application": "Athena Bid Intelligence System",
            "status": "running",
            "version": "0.1.0"
        }

    @app.route("/health")
    def health():

        return {
            "status": "healthy"
        }

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)