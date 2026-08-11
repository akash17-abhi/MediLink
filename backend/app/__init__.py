from dotenv import load_dotenv

load_dotenv()   

from flask import Flask

from .config import Config
from .extensions import (
    db,
    migrate,
    jwt,
    cors,
    socketio,
)

from app.services.email_service import EmailService

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    socketio.init_app(app)
    #Initialize Email Service
    EmailService.init_app(app)

    # Import all models so Flask-Migrate can detect them
    from app import models

    # Register all routes
    from app.routes import register_routes
    register_routes(app)

    @app.route("/")
    def home():
        return {
            "success": True,
            "project": "MediLink",
            "message": "Backend is running successfully",
            "version": "1.0.0"
        }

    return app