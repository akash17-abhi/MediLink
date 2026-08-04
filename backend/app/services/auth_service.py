from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models.user import User


class AuthService:

    @staticmethod
    def register(data):

        hashed_password = generate_password_hash(data["password"])

        user = User(
            full_name=data["full_name"],
            email=data["email"],
            password_hash=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        return user