from app.extensions import db
from app.models.role import Role
from app.models.user import User


class RoleService:

    # =========================================================
    # CREATE ROLE
    # =========================================================

    @staticmethod
    def create_role(name, description=None):

        existing_role = Role.query.filter_by(
            name=name
        ).first()

        if existing_role:
            return None, "Role already exists"

        role = Role(
            name=name,
            description=description
        )

        db.session.add(role)
        db.session.commit()

        return role, None

    # =========================================================
    # GET ALL ROLES
    # =========================================================

    @staticmethod
    def get_all_roles():

        return Role.query.order_by(
            Role.id.asc()
        ).all()

    # =========================================================
    # GET ROLE BY NAME
    # =========================================================

    @staticmethod
    def get_role_by_name(name):

        return Role.query.filter_by(
            name=name
        ).first()

    # =========================================================
    # GET ROLE BY ID
    # =========================================================

    @staticmethod
    def get_role_by_id(role_id):

        return Role.query.get(role_id)

    # =========================================================
    # ASSIGN ROLE TO USER
    # =========================================================

    @staticmethod
    def assign_role(user_id, role_name):

        user = User.query.get(user_id)

        if not user:
            return None, "User not found"

        role = Role.query.filter_by(
            name=role_name
        ).first()

        if not role:
            return None, "Role not found"

        # Prevent duplicate role assignment
        if role in user.roles:
            return None, "User already has this role"

        user.roles.append(role)

        db.session.commit()

        return role, None

    # =========================================================
    # REMOVE ROLE FROM USER
    # =========================================================

    @staticmethod
    def remove_role(user_id, role_name):

        user = User.query.get(user_id)

        if not user:
            return False, "User not found"

        role = Role.query.filter_by(
            name=role_name
        ).first()

        if not role:
            return False, "Role not found"

        if role not in user.roles:
            return False, "User does not have this role"

        user.roles.remove(role)

        db.session.commit()

        return True, None

    # =========================================================
    # CHECK USER ROLE
    # =========================================================

    @staticmethod
    def has_role(user_id, role_name):

        user = User.query.get(user_id)

        if not user:
            return False

        return any(
            role.name == role_name
            for role in user.roles
        )

    # =========================================================
    # GET USER ROLES
    # =========================================================

    @staticmethod
    def get_user_roles(user_id):

        user = User.query.get(user_id)

        if not user:
            return None

        return user.roles