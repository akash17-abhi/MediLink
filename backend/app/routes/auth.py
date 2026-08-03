from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.get("/")
def auth_home():
    return {
        "success": True,
        "message": "Authentication API is working"
    }