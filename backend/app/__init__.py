# from dotenv import load_dotenv

# load_dotenv()

# from flask import Flask

# from .config import Config

# from .extensions import (
#     db,
#     migrate,
#     jwt,
#     cors,
#     socketio,
# )

# from app.services.email_service import EmailService


# def create_app():

#     app = Flask(__name__)

#     # =====================================================
#     # APPLICATION CONFIGURATION
#     # =====================================================

#     app.config.from_object(Config)

#     # =====================================================
#     # INITIALIZE EXTENSIONS
#     # =====================================================

#     db.init_app(app)

#     migrate.init_app(
#         app,
#         db
#     )

#     jwt.init_app(app)

#     cors.init_app(app)

#     socketio.init_app(app)

#     # =====================================================
#     # INITIALIZE EMAIL SERVICE
#     # =====================================================

#     EmailService.init_app(app)

#     # =====================================================
#     # IMPORT ALL MODELS
#     # =====================================================
#     # This allows Flask-Migrate to detect all models.

#     from app import models

#     # =====================================================
#     # REGISTER ALL ROUTES
#     # =====================================================
#     # All blueprints, including the Ambulance blueprint
#     # and chatbot blueprint, are registered centrally
#     # from app.routes.register_routes.

#     from app.routes import register_routes

#     register_routes(app)

#     # =====================================================
#     # HOME ROUTE
#     # =====================================================

#     @app.route("/")
#     def home():

#         return {
#             "success": True,
#             "project": "MediLink",
#             "message": "Backend is running successfully",
#             "version": "1.0.0"
#         }

#     # =====================================================
#     # RETURN APPLICATION
#     # =====================================================

#     return app


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

    # =====================================================
    # APPLICATION CONFIGURATION
    # =====================================================

    app.config.from_object(Config)

    # =====================================================
    # INITIALIZE EXTENSIONS
    # =====================================================

    db.init_app(app)

    migrate.init_app(
        app,
        db
    )

    jwt.init_app(app)

    # Enable CORS for frontend domains (Vercel, localhost, and production)
    cors.init_app(
        app,
        resources={r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"]
        }}
    )

    # Enable SocketIO CORS
    socketio.init_app(
        app,
        cors_allowed_origins="*"
    )

    # =====================================================
    # INITIALIZE EMAIL SERVICE
    # =====================================================

    EmailService.init_app(app)

    # =====================================================
    # IMPORT ALL MODELS
    # =====================================================

    from app import models

    # =====================================================
    # REGISTER ALL ROUTES
    # =====================================================

    from app.routes import register_routes

    register_routes(app)

    # =====================================================
    # HOME ROUTE
    # =====================================================

    @app.route("/")
    def home():

        return {
            "success": True,
            "project": "MediLink",
            "message": "Backend is running successfully",
            "version": "1.0.0"
        }

    # =====================================================
    # RETURN APPLICATION
    # =====================================================

    return app