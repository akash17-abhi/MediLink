from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models.user import User


class AuthService:

    @staticmethod
    def register(data):

        existing_user = User.query.filter_by(email=data["email"]).first()

        if existing_user:
            return None, "Email already exists"

        hashed_password = generate_password_hash(data["password"])

        user = User(
            full_name=data["full_name"],
            email=data["email"],
            password_hash=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        return user, None

    @staticmethod
    def login(data):

        user = User.query.filter_by(email=data["email"]).first()

        if not user:
            return None, "Invalid email"

        if not check_password_hash(user.password_hash, data["password"]):
            return None, "Invalid password"

        return user, None