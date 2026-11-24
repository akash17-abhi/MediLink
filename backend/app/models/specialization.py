from app.extensions import db
from app.models.base_model import BaseModel


class Specialization(BaseModel):
    """
    Medical specialization / clinical department model.
    Maps to hospital departments (e.g., Cardiology, Orthopedics, Neurology).
    """

    __tablename__ = "specializations"

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    icon = db.Column(
        db.String(50),
        default="Activity"
    )

    is_emergency = db.Column(
        db.Boolean,
        default=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "icon": self.icon,
            "is_emergency": self.is_emergency,
            "is_active": self.is_active
        }

    def __repr__(self):
        return f"<Specialization {self.code}: {self.name}>"
