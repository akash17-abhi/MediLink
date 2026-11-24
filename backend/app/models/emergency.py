from app.extensions import db
from app.models.base_model import BaseModel


class Emergency(BaseModel):

    __tablename__ = "emergencies"

    # =========================================================
    # PATIENT
    # =========================================================

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=False
    )

    # =========================================================
    # HOSPITAL
    # =========================================================

    hospital_id = db.Column(
        db.Integer,
        db.ForeignKey("hospitals.id"),
        nullable=True
    )

    # =========================================================
    # AMBULANCE
    # =========================================================

    ambulance_id = db.Column(
        db.Integer,
        db.ForeignKey("ambulances.id"),
        nullable=True
    )

    # =========================================================
    # EMERGENCY INFORMATION
    # =========================================================

    emergency_type = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    priority = db.Column(
        db.String(20),
        default="Medium",
        nullable=False
    )

    # =========================================================
    # LOCATION
    # =========================================================

    pickup_location = db.Column(
        db.String(500),
        nullable=False
    )

    destination = db.Column(
        db.String(500),
        nullable=True
    )

    # =========================================================
    # STATUS
    # =========================================================

    status = db.Column(
        db.String(50),
        default="Requested",
        nullable=False
    )

    # =========================================================
    # RELATIONSHIPS
    # =========================================================

    patient = db.relationship(
        "Patient",
        backref="emergencies"
    )

    hospital = db.relationship(
        "Hospital",
        backref="emergencies"
    )

    ambulance = db.relationship(
        "Ambulance",
        backref="emergencies"
    )

    # =========================================================
    # REPRESENTATION
    # =========================================================

    def __repr__(self):

        return f"<Emergency {self.id} - {self.status}>"