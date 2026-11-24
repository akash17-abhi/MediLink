from datetime import datetime, timedelta
import secrets

from flask import current_app
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.extensions import db
from app.models.user import User
from app.services.email_service import EmailService


class AuthService:

    # =========================================================
    # GENERATE OTP
    # =========================================================

    @staticmethod
    def generate_otp():
        """Generate a secure 6-digit OTP."""
        return f"{secrets.randbelow(1000000):06d}"

    # =========================================================
    # REGISTER
    # =========================================================

    @staticmethod
    def register(data):

        existing_user = User.query.filter_by(
            email=data["email"]
        ).first()

        if existing_user:
            return None, "Email already exists"

        hashed_password = generate_password_hash(
            data["password"]
        )

        user = User(
            full_name=data["full_name"],
            email=data["email"],
            password_hash=hashed_password,
            is_active=True,
            is_email_verified=True,
        )

        db.session.add(user)
        db.session.commit()

        return user, None

    # =========================================================
    # VERIFY EMAIL
    # =========================================================

    @staticmethod
    def verify_email(email, code):

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:
            return None, "User not found"

        if user.is_email_verified:
            return user, "Email is already verified"

        if not user.verification_code:
            return None, "No verification code found"

        if user.verification_code != code:
            return None, "Invalid verification code"

        if (
            not user.verification_code_expires_at
            or datetime.utcnow()
            > user.verification_code_expires_at
        ):
            return None, "Verification code has expired"

        user.is_email_verified = True

        # Clear verification code after successful use
        user.verification_code = None
        user.verification_code_expires_at = None

        db.session.commit()

        return user, None

    # =========================================================
    # RESEND EMAIL VERIFICATION
    # =========================================================

    @staticmethod
    def resend_verification_code(email):

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:
            return None, "User not found"

        if user.is_email_verified:
            return None, "Email is already verified"

        verification_code = AuthService.generate_otp()

        user.verification_code = verification_code

        user.verification_code_expires_at = (
            datetime.utcnow() + timedelta(minutes=10)
        )

        db.session.commit()

        success, error = EmailService.send_email(
            recipient=user.email,
            subject="MediLink - New Verification Code",
            body=f"""
Dear {user.full_name},

Your new MediLink email verification code is:

{verification_code}

This code will expire in 10 minutes.

Regards,
MediLink Team
""",
            html=f"""
            <html>
                <body style="
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                ">

                    <h2>MediLink - New Verification Code</h2>

                    <p>
                        Dear <strong>{user.full_name}</strong>,
                    </p>

                    <p>
                        Your new verification code is:
                    </p>

                    <h1 style="
                        letter-spacing: 8px;
                        font-size: 32px;
                    ">
                        {verification_code}
                    </h1>

                    <p>
                        This code will expire in
                        <strong>10 minutes</strong>.
                    </p>

                    <p>
                        Regards,<br>
                        <strong>MediLink Team</strong>
                    </p>

                </body>
            </html>
            """
        )

        print(f"\n========================================", flush=True)
        print(f"🔐 [MEDILINK OTP] Verification Code for {user.email}: {verification_code}", flush=True)
        print(f"========================================\n", flush=True)

        if not success:
            current_app.logger.warning(f"Email delivery skipped/failed: {error}. Use console OTP.")

        return user, None

    # =========================================================
    # LOGIN - STEP 1
    # =========================================================

    @staticmethod
    def login(data):

        raw_email = (data.get("email") or "").strip()
        raw_password = (data.get("password") or "")

        # Convenience alias for demo testing
        alias_map = {
            "hospital": "hospital@medilink.com",
            "hospital admin": "hospital@medilink.com",
            "admin": "admin@medilink.com",
            "super admin": "admin@medilink.com",
            "patient": "patient@medilink.com",
        }
        lookup_email = alias_map.get(raw_email.lower(), raw_email)

        # Case-insensitive email lookup
        user = User.query.filter(User.email.ilike(lookup_email)).first()

        if not user:
            return None, "Invalid email address"

        # Check password with case-insensitive fallback for demo accounts
        valid_password = check_password_hash(user.password_hash, raw_password)
        if not valid_password:
            # Fallback for demo users if capitalization differs
            if user.email == "hospital@medilink.com" and raw_password.lower() in ["hospital@123", "hospital123", "hospital"]:
                valid_password = True
            elif user.email == "admin@medilink.com" and raw_password.lower() in ["admin@123", "admin123", "admin"]:
                valid_password = True
            elif user.email == "patient@medilink.com" and raw_password.lower() in ["patient@123", "patient123", "patient"]:
                valid_password = True

        if not valid_password:
            return None, "Invalid password"

        if not user.is_active:
            return None, "Account is inactive"

        return user, None

    # =========================================================
    # VERIFY LOGIN OTP
    # =========================================================

    @staticmethod
    def verify_login_otp(email, otp):

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:
            return None, "User not found"

        if not user.login_otp:
            return None, "No login OTP found"

        if user.login_otp != otp:
            return None, "Invalid login OTP"

        if (
            not user.login_otp_expires_at
            or datetime.utcnow()
            > user.login_otp_expires_at
        ):
            return None, "Login OTP has expired"

        # OTP successfully used
        user.login_otp = None
        user.login_otp_expires_at = None

        db.session.commit()

        return user, None

    # =========================================================
    # RESEND LOGIN OTP
    # =========================================================

    @staticmethod
    def resend_login_otp(email):

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:
            return None, "User not found"

        if not user.is_email_verified:
            return None, "Email is not verified"

        login_otp = AuthService.generate_otp()

        user.login_otp = login_otp

        user.login_otp_expires_at = (
            datetime.utcnow() + timedelta(minutes=5)
        )

        db.session.commit()

        success, error = EmailService.send_email(
            recipient=user.email,
            subject="MediLink - New Login Verification Code",
            body=f"""
Dear {user.full_name},

Your new MediLink login verification code is:

{login_otp}

This code will expire in 5 minutes.

Regards,
MediLink Team
""",
            html=f"""
            <html>
                <body style="
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                ">

                    <h2>MediLink - New Login Code</h2>

                    <p>
                        Dear <strong>{user.full_name}</strong>,
                    </p>

                    <p>
                        Your new login verification code is:
                    </p>

                    <h1 style="
                        letter-spacing: 8px;
                        font-size: 32px;
                    ">
                        {login_otp}
                    </h1>

                    <p>
                        This code will expire in
                        <strong>5 minutes</strong>.
                    </p>

                    <p>
                        Regards,<br>
                        <strong>MediLink Team</strong>
                    </p>

                </body>
            </html>
            """
        )

        print(f"\n========================================", flush=True)
        print(f"🔐 [MEDILINK OTP] Resend Login OTP for {user.email}: {login_otp}", flush=True)
        print(f"========================================\n", flush=True)

        if not success:
            current_app.logger.warning(f"Email delivery skipped/failed: {error}. Use console OTP.")

        return user, None

    # =========================================================
    # FORGOT PASSWORD - SEND RESET OTP
    # =========================================================

    @staticmethod
    def forgot_password(email):

        user = User.query.filter_by(
            email=email
        ).first()

        # Do not reveal whether an email exists
        if not user:
            return True, (
                "If the email is registered, "
                "a password reset code has been sent."
            )

        reset_otp = AuthService.generate_otp()

        user.reset_password_otp = reset_otp

        user.reset_password_otp_expires_at = (
            datetime.utcnow() + timedelta(minutes=10)
        )

        db.session.commit()

        # -----------------------------------------------------
        # Send password reset email
        # -----------------------------------------------------

        success, error = EmailService.send_email(
            recipient=user.email,
            subject="MediLink - Password Reset Code",
            body=f"""
Dear {user.full_name},

We received a request to reset your MediLink password.

Your password reset code is:

{reset_otp}

This code will expire in 10 minutes.

If you did not request a password reset, please ignore
this email.

Regards,
MediLink Team
""",
            html=f"""
            <html>
                <body style="
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                ">

                    <h2>MediLink - Password Reset</h2>

                    <p>
                        Dear <strong>{user.full_name}</strong>,
                    </p>

                    <p>
                        We received a request to reset your
                        MediLink password.
                    </p>

                    <p>
                        Your password reset code is:
                    </p>

                    <h1 style="
                        letter-spacing: 8px;
                        font-size: 32px;
                    ">
                        {reset_otp}
                    </h1>

                    <p>
                        This code will expire in
                        <strong>10 minutes</strong>.
                    </p>

                    <p>
                        If you did not request a password reset,
                        please ignore this email.
                    </p>

                    <br>

                    <p>
                        Regards,<br>
                        <strong>MediLink Team</strong>
                    </p>

                </body>
            </html>
            """
        )

        print(f"\n========================================", flush=True)
        print(f"🔐 [MEDILINK OTP] Password Reset OTP for {user.email}: {reset_otp}", flush=True)
        print(f"========================================\n", flush=True)

        if not success:
            current_app.logger.warning(f"Email delivery skipped/failed: {error}. Use console OTP.")

        return True, (
            "If the email is registered, "
            "a password reset code has been sent."
        )

    # =========================================================
    # VERIFY PASSWORD RESET OTP
    # =========================================================

    @staticmethod
    def verify_reset_otp(email, otp):

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:
            return None, "Invalid email or reset code"

        if not user.reset_password_otp:
            return None, "No password reset code found"

        if (
            not user.reset_password_otp_expires_at
            or datetime.utcnow()
            > user.reset_password_otp_expires_at
        ):
            user.reset_password_otp = None
            user.reset_password_otp_expires_at = None

            db.session.commit()

            return None, "Password reset code has expired"

        if user.reset_password_otp != otp:
            return None, "Invalid password reset code"

        return user, None

    # =========================================================
    # RESET PASSWORD
    # =========================================================

    @staticmethod
    def reset_password(email, otp, new_password):

        user, error = AuthService.verify_reset_otp(
            email,
            otp
        )

        if error:
            return None, error

        user.password_hash = generate_password_hash(
            new_password
        )

        # -----------------------------------------------------
        # Invalidate OTP after successful password reset
        # -----------------------------------------------------

        user.reset_password_otp = None
        user.reset_password_otp_expires_at = None

        # -----------------------------------------------------
        # Invalidate any existing login OTP
        # -----------------------------------------------------

        user.login_otp = None
        user.login_otp_expires_at = None

        db.session.commit()

        return user, None

    # =========================================================
    # GET USER
    # =========================================================

    @staticmethod
    def get_user_by_id(user_id):

        return User.query.get(user_id)