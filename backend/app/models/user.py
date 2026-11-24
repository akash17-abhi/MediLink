# from app.extensions import db
# from .base_model import BaseModel


# class User(BaseModel):

#     __tablename__ = "users"

#     # =========================================================
#     # BASIC INFORMATION
#     # =========================================================

#     full_name = db.Column(
#         db.String(100),
#         nullable=False
#     )

#     email = db.Column(
#         db.String(120),
#         unique=True,
#         nullable=False
#     )

#     password_hash = db.Column(
#         db.String(255),
#         nullable=False
#     )

#     is_active = db.Column(
#         db.Boolean,
#         default=True
#     )

#     # =========================================================
#     # EMAIL VERIFICATION
#     # =========================================================

#     is_email_verified = db.Column(
#         db.Boolean,
#         default=False,
#         nullable=False,
#         server_default="0"
#     )

#     verification_code = db.Column(
#         db.String(6),
#         nullable=True
#     )

#     verification_code_expires_at = db.Column(
#         db.DateTime,
#         nullable=True
#     )

#     # =========================================================
#     # LOGIN OTP
#     # =========================================================

#     login_otp = db.Column(
#         db.String(6),
#         nullable=True
#     )

#     login_otp_expires_at = db.Column(
#         db.DateTime,
#         nullable=True
#     )

#     # =========================================================
#     # PASSWORD RESET
#     # =========================================================

#     reset_password_otp = db.Column(
#         db.String(6),
#         nullable=True
#     )

#     reset_password_otp_expires_at = db.Column(
#         db.DateTime,
#         nullable=True
#     )

#     # =========================================================
#     # ROLES
#     # =========================================================

#     roles = db.relationship(
#         "Role",
#         secondary="user_roles",
#         back_populates="users"
#     )

#     # =========================================================
#     # HOSPITAL
#     # =========================================================

#     hospital = db.relationship(
#         "Hospital",
#         back_populates="user",
#         uselist=False
#     )

#     # =========================================================
#     # REPRESENTATION
#     # =========================================================

#     def __repr__(self):
#         return f"<User {self.email}>"

from datetime import datetime, timedelta, timezone
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

    login_otp_created_at = db.Column(
        db.DateTime,
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
    # HELPER METHODS FOR LOGIN OTP
    # =========================================================

    def set_login_otp(self, otp_code: str, valid_minutes: int = 2):
        """Sets a new login OTP along with created_at and expires_at timestamps."""
        now = datetime.now(timezone.utc)
        self.login_otp = otp_code
        self.login_otp_created_at = now
        self.login_otp_expires_at = now + timedelta(minutes=valid_minutes)

    def is_login_otp_valid(self, input_otp: str) -> bool:
        """Validates if the provided OTP matches and has not expired."""
        if not self.login_otp or not self.login_otp_expires_at:
            return False

        if self.login_otp != input_otp:
            return False

        now = datetime.now(timezone.utc)
        expires_at = self.login_otp_expires_at

        # Ensure timezone awareness compatibility
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        return now <= expires_at

    def can_resend_login_otp(self, cooldown_seconds: int = 120) -> tuple[bool, int]:
        """
        Checks if enough time has passed before allowing a resend.
        Returns a tuple: (can_resend: bool, seconds_remaining: int)
        """
        if not self.login_otp_created_at:
            return True, 0

        now = datetime.now(timezone.utc)
        created_at = self.login_otp_created_at

        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        elapsed_seconds = (now - created_at).total_seconds()

        if elapsed_seconds < cooldown_seconds:
            remaining_seconds = int(cooldown_seconds - elapsed_seconds)
            return False, remaining_seconds

        return True, 0

    def clear_login_otp(self):
        """Clears the stored login OTP after successful verification."""
        self.login_otp = None
        self.login_otp_created_at = None
        self.login_otp_expires_at = None

    # =========================================================
    # REPRESENTATION
    # =========================================================

    def __repr__(self):
        return f"<User {self.email}>"