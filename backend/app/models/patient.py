# backend/app/models/patient.py

from app import db
from app.models.base_model import BaseModel
from datetime import datetime, date


class Patient(BaseModel):
    """Patient model extending BaseModel"""

    __tablename__ = "patients"

    # =========================================================
    # PERSONAL INFORMATION
    # =========================================================

    full_name = db.Column(
        db.String(255),
        nullable=False
    )

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    gender = db.Column(
        db.String(10),
        nullable=False
    )

    date_of_birth = db.Column(
        db.Date,
        nullable=False
    )

    age = db.Column(
        db.Integer
    )

    # =========================================================
    # MEDICAL INFORMATION
    # =========================================================

    blood_group = db.Column(
        db.String(5)
    )

    allergies = db.Column(
        db.Text
    )

    chronic_conditions = db.Column(
        db.Text
    )

    current_medications = db.Column(
        db.Text
    )

    medical_history = db.Column(
        db.Text
    )

    # =========================================================
    # ADDRESS
    # =========================================================

    address = db.Column(
        db.Text
    )

    city = db.Column(
        db.String(100)
    )

    state = db.Column(
        db.String(100)
    )

    pincode = db.Column(
        db.String(10)
    )

    country = db.Column(
        db.String(100),
        default="India"
    )

    # =========================================================
    # EMERGENCY CONTACT
    # =========================================================

    emergency_contact_name = db.Column(
        db.String(255)
    )

    emergency_contact_phone = db.Column(
        db.String(20)
    )

    emergency_contact_relation = db.Column(
        db.String(50)
    )

    # =========================================================
    # PROFILE
    # =========================================================

    profile_photo = db.Column(
        db.String(500)
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    is_verified = db.Column(
        db.Boolean,
        default=False
    )

    # =========================================================
    # INSURANCE
    # =========================================================

    insurance_provider = db.Column(
        db.String(255)
    )

    insurance_policy_number = db.Column(
        db.String(100)
    )

    insurance_valid_until = db.Column(
        db.Date
    )

    # =========================================================
    # USER RELATIONSHIP
    # =========================================================

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Convert string DOB to Python date
        if isinstance(self.date_of_birth, str):
            self.date_of_birth = datetime.strptime(
                self.date_of_birth,
                "%Y-%m-%d"
            ).date()

        # Calculate age automatically
        if self.date_of_birth and self.age is None:
            today = date.today()

            self.age = (
                today.year
                - self.date_of_birth.year
                - (
                    (today.month, today.day)
                    < (
                        self.date_of_birth.month,
                        self.date_of_birth.day,
                    )
                )
            )

    # =========================================================
    # SERIALIZATION
    # =========================================================

    def to_dict(self):

        return {
            "id": self.id,

            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "gender": self.gender,

            "date_of_birth": (
                self.date_of_birth.strftime("%Y-%m-%d")
                if self.date_of_birth
                else None
            ),

            "age": self.age,

            "blood_group": self.blood_group,
            "allergies": self.allergies,
            "chronic_conditions": self.chronic_conditions,
            "current_medications": self.current_medications,
            "medical_history": self.medical_history,

            "address": self.address,
            "city": self.city,
            "state": self.state,
            "pincode": self.pincode,
            "country": self.country,

            "emergency_contact_name": self.emergency_contact_name,
            "emergency_contact_phone": self.emergency_contact_phone,
            "emergency_contact_relation": self.emergency_contact_relation,

            "profile_photo": self.profile_photo,
            "active": self.active,
            "is_verified": self.is_verified,

            "insurance_provider": self.insurance_provider,
            "insurance_policy_number": self.insurance_policy_number,

            "insurance_valid_until": (
                self.insurance_valid_until.strftime("%Y-%m-%d")
                if self.insurance_valid_until
                else None
            ),

            "user_id": self.user_id,

            "created_at": (
                self.created_at.strftime("%Y-%m-%d %H:%M:%S")
                if self.created_at
                else None
            ),

            "updated_at": (
                self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                if self.updated_at
                else None
            ),
        }

    # =========================================================
    # REPRESENTATION
    # =========================================================

    def __repr__(self):

        return f"<Patient {self.full_name}>"