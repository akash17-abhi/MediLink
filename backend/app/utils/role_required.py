from functools import wraps

from flask import jsonify
from flask_jwt_extended import (
    get_jwt_identity,
    verify_jwt_in_request
)

from app.services.role_service import RoleService


def role_required(*required_roles):
    """
    Restrict an API endpoint to users who have
    at least one of the specified roles.

    Example:

        @role_required("Admin")

    Or:

        @role_required("Admin", "Hospital")
    """

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            # -------------------------------------------------
            # Verify JWT
            # -------------------------------------------------

            try:
                verify_jwt_in_request()

            except Exception:

                return jsonify({
                    "success": False,
                    "message": "Authentication required"
                }), 401

            # -------------------------------------------------
            # Get logged-in user
            # -------------------------------------------------

            user_id = get_jwt_identity()

            if not user_id:

                return jsonify({
                    "success": False,
                    "message": "Invalid authentication token"
                }), 401

            # -------------------------------------------------
            # Check user roles
            # -------------------------------------------------

            user_roles = RoleService.get_user_roles(
                int(user_id)
            )

            if user_roles is None:

                return jsonify({
                    "success": False,
                    "message": "User not found"
                }), 404

            user_role_names = {
                role.name
                for role in user_roles
            }

            # -------------------------------------------------
            # Check permission
            # -------------------------------------------------

            if not any(
                role in user_role_names
                for role in required_roles
            ):

                return jsonify({
                    "success": False,
                    "message": "You do not have permission to access this resource"
                }), 403

            # -------------------------------------------------
            # Permission granted
            # -------------------------------------------------

            return function(*args, **kwargs)

        return wrapper

    return decorator