from app.extensions import db
from app.models.base_model import BaseModel


class Bed(BaseModel):

    __tablename__ = "beds"

    # =========================================================
    # HOSPITAL
    # =========================================================

    hospital_id = db.Column(
        db.Integer,
        db.ForeignKey("hospitals.id"),
        nullable=False
    )

    # =========================================================
    # BED INFORMATION
    # =========================================================

    bed_number = db.Column(
        db.String(50),
        nullable=False
    )

    ward = db.Column(
        db.String(100),
        nullable=False
    )

    bed_type = db.Column(
        db.String(50),
        nullable=False
    )

    floor = db.Column(
        db.String(50)
    )

    room_number = db.Column(
        db.String(50)
    )

    # =========================================================
    # BED STATUS
    # =========================================================

    status = db.Column(
        db.String(50),
        default="Available",
        nullable=False
    )

    # =========================================================
    # PATIENT
    # =========================================================

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=True
    )

    # =========================================================
    # ADDITIONAL INFORMATION
    # =========================================================

    notes = db.Column(
        db.Text
    )

    # =========================================================
    # RELATIONSHIPS
    # =========================================================

    hospital = db.relationship(
        "Hospital",
        backref="beds"
    )

    patient = db.relationship(
        "Patient",
        backref="assigned_beds"
    )

    # =========================================================
    # REPRESENTATION
    # =========================================================

    def __repr__(self):

        return f"<Bed {self.bed_number} - {self.status}>"