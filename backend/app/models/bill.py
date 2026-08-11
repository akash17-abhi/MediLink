from app.extensions import db
from app.models.base_model import BaseModel


class Bill(BaseModel):

    __tablename__ = "bills"

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=False
    )

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey("doctors.id"),
        nullable=False
    )

    hospital_id = db.Column(
        db.Integer,
        db.ForeignKey("hospitals.id"),
        nullable=False
    )

    consultation_charge = db.Column(
        db.Float,
        default=0
    )

    laboratory_charge = db.Column(
        db.Float,
        default=0
    )

    medicine_charge = db.Column(
        db.Float,
        default=0
    )

    other_charge = db.Column(
        db.Float,
        default=0
    )

    discount = db.Column(
        db.Float,
        default=0
    )

    tax = db.Column(
        db.Float,
        default=0
    )

    total_amount = db.Column(
        db.Float,
        default=0
    )

    payment_status = db.Column(
        db.String(50),
        default="Pending"
    )

    patient = db.relationship(
        "Patient",
        backref="bills"
    )

    doctor = db.relationship(
        "Doctor",
        backref="bills"
    )

    hospital = db.relationship(
        "Hospital",
        backref="bills"
    )