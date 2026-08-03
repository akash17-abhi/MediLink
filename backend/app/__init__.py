from flask import Flask, app

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

    db.init_app(app)
    from app import models
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    socketio.init_app(app)
    from app.routes.auth import auth_bp

    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():
        return {
            "success": True,
            "project": "MediLink",
            "message": "Backend is running successfully",
            "version": "1.0.0"
        }

    return app