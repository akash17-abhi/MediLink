from app.extensions import db
from .base_model import BaseModel


class Role(BaseModel):
    __tablename__ = "roles"

    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))

    users = db.relationship(
        "User",
        secondary="user_roles",
        back_populates="roles"
    )

    def __repr__(self):
        return f"<Role {self.name}>"