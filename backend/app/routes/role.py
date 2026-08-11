from flask import Blueprint, request

from app.services.role_service import RoleService
from app.utils.role_required import role_required


role_bp = Blueprint(
    "role",
    __name__,
    url_prefix="/api/roles"
)


# =========================================================
# GET ALL ROLES
# ADMIN ONLY
# =========================================================

@role_bp.get("/")
@role_required("Admin")
def get_all_roles():

    roles = RoleService.get_all_roles()

    return {
        "success": True,
        "count": len(roles),
        "roles": [
            {
                "id": role.id,
                "name": role.name,
                "description": role.description
            }
            for role in roles
        ]
    }, 200


# =========================================================
# GET USER ROLES
# ADMIN ONLY
# =========================================================

@role_bp.get("/user/<int:user_id>")
@role_required("Admin")
def get_user_roles(user_id):

    roles = RoleService.get_user_roles(user_id)

    if roles is None:

        return {
            "success": False,
            "message": "User not found"
        }, 404

    return {
        "success": True,
        "user_id": user_id,
        "roles": [
            {
                "id": role.id,
                "name": role.name,
                "description": role.description
            }
            for role in roles
        ]
    }, 200


# =========================================================
# ASSIGN ROLE
# ADMIN ONLY
# =========================================================

@role_bp.post("/user/<int:user_id>")
@role_required("Admin")
def assign_role(user_id):

    data = request.get_json() or {}

    role_name = data.get("role")

    if not role_name:

        return {
            "success": False,
            "message": "Role is required"
        }, 400

    role, error = RoleService.assign_role(
        user_id,
        role_name
    )

    if error:

        return {
            "success": False,
            "message": error
        }, 400

    return {
        "success": True,
        "message": "Role assigned successfully",
        "user_id": user_id,
        "role": {
            "id": role.id,
            "name": role.name,
            "description": role.description
        }
    }, 200


# =========================================================
# REMOVE ROLE
# ADMIN ONLY
# =========================================================

@role_bp.delete("/user/<int:user_id>")
@role_required("Admin")
def remove_role(user_id):

    data = request.get_json() or {}

    role_name = data.get("role")

    if not role_name:

        return {
            "success": False,
            "message": "Role is required"
        }, 400

    success, error = RoleService.remove_role(
        user_id,
        role_name
    )

    if not success:

        return {
            "success": False,
            "message": error
        }, 400

    return {
        "success": True,
        "message": "Role removed successfully"
    }, 200