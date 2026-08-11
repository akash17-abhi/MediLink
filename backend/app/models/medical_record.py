from app.extensions import db
from app.models.base_model import BaseModel


class MedicalRecord(BaseModel):
    __tablename__ = "medical_records"

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

    appointment_id = db.Column(
        db.Integer,
        db.ForeignKey("appointments.id"),
        nullable=True
    )

    diagnosis = db.Column(db.Text, nullable=False)

    symptoms = db.Column(db.Text)

    prescription = db.Column(db.Text)

    lab_tests = db.Column(db.Text)

    notes = db.Column(db.Text)

    follow_up_date = db.Column(db.Date)

    patient = db.relationship("Patient", backref="medical_records")

    doctor = db.relationship("Doctor", backref="medical_records")

    appointment = db.relationship("Appointment", backref="medical_record")