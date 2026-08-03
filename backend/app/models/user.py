from app.extensions import db
from .base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    full_name = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    roles = db.relationship(
        "Role",
        secondary="user_roles",
        back_populates="users"
    )

    def __repr__(self):
        return f"<User {self.email}>"