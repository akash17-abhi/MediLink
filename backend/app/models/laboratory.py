from app.extensions import db
from app.models.base_model import BaseModel


class Laboratory(BaseModel):

    __tablename__ = "laboratories"

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

    test_name = db.Column(
        db.String(200),
        nullable=False
    )

    category = db.Column(
        db.String(100)
    )

    status = db.Column(
        db.String(50),
        default="Pending"
    )

    result = db.Column(
        db.Text
    )

    report_file = db.Column(
        db.String(500)
    )

    patient = db.relationship(
        "Patient",
        backref="laboratory_tests"
    )

    doctor = db.relationship(
        "Doctor",
        backref="laboratory_tests"
    )

    hospital = db.relationship(
        "Hospital",
        backref="laboratory_tests"
    )