from flask import Blueprint, request
from flask_jwt_extended import create_access_token

from app.schemas.auth_schema import (
    validate_register,
    validate_login
)
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

    user, error = AuthService.register(data)

    if error:
        return {
            "success": False,
            "message": error
        }, 409

    return {
        "success": True,
        "message": "Registration successful",
        "user": {
            "id": user.id,
            "name": user.full_name,
            "email": user.email
        }
    }, 201


@auth_bp.post("/login")
def login():

    data = request.get_json()

    valid, message = validate_login(data)

    if not valid:
        return {
            "success": False,
            "message": message
        }, 400

    user, error = AuthService.login(data)

    if error:
        return {
            "success": False,
            "message": error
        }, 401

    access_token = create_access_token(identity=str(user.id))

    return {
        "success": True,
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "name": user.full_name,
            "email": user.email
        }
    }, 200