from app.extensions import db
from .base_model import BaseModel


class Hospital(BaseModel):
    __tablename__ = "hospitals"

    # Basic Information
    name = db.Column(
        db.String(150),
        nullable=False
    )

    registration_number = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    hospital_type = db.Column(
        db.String(50),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    # Contact Information
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=False
    )

    emergency_contact = db.Column(
        db.String(20)
    )

    website = db.Column(
        db.String(255)
    )

    # Address
    address = db.Column(
        db.Text,
        nullable=False
    )

    city = db.Column(
        db.String(100),
        nullable=False
    )

    state = db.Column(
        db.String(100),
        nullable=False
    )

    pincode = db.Column(
        db.String(10),
        nullable=False
    )

    latitude = db.Column(
        db.Float
    )

    longitude = db.Column(
        db.Float
    )

    # Hospital Capacity
    total_beds = db.Column(
        db.Integer,
        default=0
    )

    icu_beds = db.Column(
        db.Integer,
        default=0
    )

    emergency_beds = db.Column(
        db.Integer,
        default=0
    )

    operation_theatres = db.Column(
        db.Integer,
        default=0
    )

    # Working Hours
    opening_time = db.Column(
        db.String(10)
    )

    closing_time = db.Column(
        db.String(10)
    )

    is_24x7 = db.Column(
        db.Boolean,
        default=False
    )

    # Media
    logo = db.Column(
        db.String(255)
    )

    banner = db.Column(
        db.String(255)
    )

    # Status
    is_verified = db.Column(
        db.Boolean,
        default=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )
    doctors = db.relationship(
    "Doctor",
    back_populates="hospital",
    lazy=True,
    cascade="all, delete-orphan"
)

    def __repr__(self):
        return f"<Hospital {self.name}>"
    