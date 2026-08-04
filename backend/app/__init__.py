from flask import Flask

from .config import Config
from .extensions import (
    db,
    migrate,
    jwt,
    cors,
    socketio,
)


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    socketio.init_app(app)

    # Import all database models
    from app import models

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.hospital import hospital_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(hospital_bp)

    @app.route("/")
    def home():
        return {
            "success": True,
            "project": "MediLink",
            "message": "Backend is running successfully",
            "version": "1.0.0"
        }

    return app