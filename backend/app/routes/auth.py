from flask import Blueprint, request

from app.schemas.auth_schema import validate_register
from app.services.auth_service import AuthService

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


@auth_bp.get("/")
def auth_home():

    return {
        "success": True,
        "message": "Authentication API is working"
    }


@auth_bp.post("/register")
def register():

    data = request.get_json()

    valid, message = validate_register(data)

    if not valid:

        return {
            "success": False,
            "message": message
        }, 400

    user = AuthService.register(data)

    return {

        "success": True,

        "message": "Registration successful",

        "user": {
            "id": user.id,
            "name": user.full_name,
            "email": user.email
        }

    }, 201