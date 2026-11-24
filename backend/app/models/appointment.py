from app.extensions import db
from .base_model import BaseModel


class Appointment(BaseModel):

    __tablename__ = "appointments"

    # =========================================================
    # PATIENT
    # =========================================================

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=False
    )

    # =========================================================
    # DOCTOR
    # =========================================================

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey("doctors.id"),
        nullable=False
    )

    # =========================================================
    # HOSPITAL
    # =========================================================

    hospital_id = db.Column(
        db.Integer,
        db.ForeignKey("hospitals.id"),
        nullable=False
    )

    # =========================================================
    # APPOINTMENT DATE
    # =========================================================

    appointment_date = db.Column(
        db.Date,
        nullable=False
    )

    # =========================================================
    # APPOINTMENT TIME
    # =========================================================

    appointment_time = db.Column(
        db.Time,
        nullable=False
    )

    # =========================================================
    # APPOINTMENT INFORMATION
    # =========================================================

    reason = db.Column(
        db.Text,
        nullable=True
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="Pending"
    )

    consultation_mode = db.Column(
        db.String(30),
        nullable=False,
        default="Offline"
    )

    payment_status = db.Column(
        db.String(30),
        nullable=False,
        default="Pending"
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    # =========================================================
    # PATIENT RELATIONSHIP
    # =========================================================

    patient = db.relationship(
        "Patient",
        backref="appointments"
    )

    # =========================================================
    # DOCTOR RELATIONSHIP
    # =========================================================

    doctor = db.relationship(
        "Doctor",
        backref="appointments"
    )

    # =========================================================
    # HOSPITAL RELATIONSHIP
    # =========================================================

    hospital = db.relationship(
        "Hospital",
        backref="appointments"
    )

    # =========================================================
    # REPRESENTATION
    # =========================================================

    def __repr__(self):
        return f"<Appointment {self.id}>"