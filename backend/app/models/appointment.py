from app.extensions import db
from .base_model import BaseModel


class Appointment(BaseModel):
    __tablename__ = "appointments"

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

    appointment_date = db.Column(
        db.Date,
        nullable=False
    )

    appointment_time = db.Column(
        db.Time,
        nullable=False
    )

    reason = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    consultation_mode = db.Column(
        db.String(30),
        default="Offline"
    )

    payment_status = db.Column(
        db.String(30),
        default="Pending"
    )

    notes = db.Column(
        db.Text
    )

    patient = db.relationship(
        "Patient",
        backref="appointments"
    )

    doctor = db.relationship(
        "Doctor",
        backref="appointments"
    )

    hospital = db.relationship(
        "Hospital",
        backref="appointments"
    )

    def __repr__(self):
        return f"<Appointment {self.id}>"