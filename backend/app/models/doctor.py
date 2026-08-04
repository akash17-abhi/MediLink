from app.extensions import db
from .base_model import BaseModel


class Doctor(BaseModel):
    __tablename__ = "doctors"

    full_name = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(db.String(20))

    specialization = db.Column(
        db.String(100),
        nullable=False
    )

    qualification = db.Column(db.String(200))

    experience = db.Column(
        db.Integer,
        default=0
    )

    consultation_fee = db.Column(
        db.Float,
        default=0
    )

    profile_photo = db.Column(db.String(255))

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    hospital_id = db.Column(
        db.Integer,
        db.ForeignKey("hospitals.id"),
        nullable=False
    )

    hospital = db.relationship(
        "Hospital",
        back_populates="doctors"
    )

    def __repr__(self):
        return f"<Doctor {self.full_name}>"