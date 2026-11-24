from app.extensions import db
from app.models.base_model import BaseModel


class Ambulance(BaseModel):

    __tablename__ = "ambulances"

    # =========================================================
    # HOSPITAL
    # =========================================================

    hospital_id = db.Column(
        db.Integer,
        db.ForeignKey("hospitals.id"),
        nullable=False
    )

    # =========================================================
    # AMBULANCE INFORMATION
    # =========================================================

    registration_number = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    ambulance_type = db.Column(
        db.String(100),
        nullable=False
    )

    # =========================================================
    # DRIVER INFORMATION
    # =========================================================

    driver_name = db.Column(
        db.String(150),
        nullable=False
    )

    driver_phone = db.Column(
        db.String(20),
        nullable=False
    )

    # =========================================================
    # LOCATION
    # =========================================================

    current_location = db.Column(
        db.String(255)
    )

    # =========================================================
    # STATUS
    # =========================================================

    availability_status = db.Column(
        db.String(50),
        default="Available",
        nullable=False
    )

    emergency_status = db.Column(
        db.String(50),
        default="Normal",
        nullable=False
    )

    # =========================================================
    # HOSPITAL RELATIONSHIP
    # =========================================================

    hospital = db.relationship(
        "Hospital",
        backref="ambulances"
    )

    # =========================================================
    # REPRESENTATION
    # =========================================================

    def __repr__(self):
        return f"<Ambulance {self.registration_number}>"