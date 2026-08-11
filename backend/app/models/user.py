from app.extensions import db
from .base_model import BaseModel


class User(BaseModel):

    __tablename__ = "users"

    # =========================================================
    # BASIC INFORMATION
    # =========================================================

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    # =========================================================
    # EMAIL VERIFICATION
    # =========================================================

    is_email_verified = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
        server_default="0"
    )

    verification_code = db.Column(
        db.String(6),
        nullable=True
    )

    verification_code_expires_at = db.Column(
        db.DateTime,
        nullable=True
    )

    # =========================================================
    # LOGIN OTP
    # =========================================================

    login_otp = db.Column(
        db.String(6),
        nullable=True
    )

    login_otp_expires_at = db.Column(
        db.DateTime,
        nullable=True
    )

    # =========================================================
    # PASSWORD RESET
    # =========================================================

    reset_password_otp = db.Column(
        db.String(6),
        nullable=True
    )

    reset_password_otp_expires_at = db.Column(
        db.DateTime,
        nullable=True
    )

    # =========================================================
    # ROLES
    # =========================================================

    roles = db.relationship(
        "Role",
        secondary="user_roles",
        back_populates="users"
    )

    # =========================================================
    # HOSPITAL
    # =========================================================

    hospital = db.relationship(
        "Hospital",
        back_populates="user",
        uselist=False
    )

    # =========================================================
    # REPRESENTATION
    # =========================================================

    def __repr__(self):
        return f"<User {self.email}>"