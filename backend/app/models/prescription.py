from app.extensions import db
from app.models.base_model import BaseModel


class Prescription(BaseModel):

    __tablename__ = "prescriptions"

    medical_record_id = db.Column(
        db.Integer,
        db.ForeignKey("medical_records.id"),
        nullable=False
    )

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

    medicines = db.Column(db.Text, nullable=False)

    dosage = db.Column(db.Text)

    duration = db.Column(db.String(100))

    instructions = db.Column(db.Text)

    patient = db.relationship("Patient", backref="prescriptions")

    doctor = db.relationship("Doctor", backref="prescriptions")

    medical_record = db.relationship(
        "MedicalRecord",
        backref="prescriptions"
    )