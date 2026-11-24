# from flask import Blueprint, request

# from flask_jwt_extended import (
#     create_access_token,
#     jwt_required,
#     get_jwt_identity
# )

# from app.schemas.auth_schema import (
#     validate_register,
#     validate_login
# )

# from app.services.auth_service import AuthService


# auth_bp = Blueprint(
#     "auth",
#     __name__,
#     url_prefix="/api/auth"
# )


# # ============================================================
# # AUTH HOME
# # ============================================================

# @auth_bp.get("/")
# def auth_home():

#     return {
#         "success": True,
#         "message": "Authentication API is working"
#     }


# # ============================================================
# # REGISTER
# # ============================================================

# @auth_bp.post("/register")
# def register():

#     data = request.get_json(silent=True) or {}

#     valid, message = validate_register(data)

#     if not valid:

#         return {
#             "success": False,
#             "message": message
#         }, 400

#     user, error = AuthService.register(data)

#     if error:

#         return {
#             "success": False,
#             "message": error
#         }, 409

#     return {

#         "success": True,

#         "message": (
#             "Registration successful. "
#             "Please check your email for the verification code."
#         ),

#         "user": {
#             "id": user.id,
#             "name": user.full_name,
#             "email": user.email,
#             "is_email_verified": user.is_email_verified
#         }

#     }, 201


# # ============================================================
# # VERIFY EMAIL
# # ============================================================

# @auth_bp.post("/verify-email")
# def verify_email():

#     data = request.get_json(silent=True) or {}

#     email = data.get("email")

#     # Accept the new field name "verification_code".
#     # Also accept "code" for backward compatibility.
#     verification_code = data.get("verification_code") or data.get("code")

#     if not email or not verification_code:

#         return {
#             "success": False,
#             "message": "Email and verification code are required"
#         }, 400

#     user, error = AuthService.verify_email(
#         email,
#         verification_code
#     )

#     if error:

#         return {
#             "success": False,
#             "message": error
#         }, 400

#     return {

#         "success": True,

#         "message": "Email verified successfully",

#         "user": {
#             "id": user.id,
#             "name": user.full_name,
#             "email": user.email,
#             "is_email_verified": user.is_email_verified
#         }

#     }, 200


# # ============================================================
# # RESEND EMAIL VERIFICATION
# # ============================================================

# @auth_bp.post("/resend-verification")
# def resend_verification():

#     data = request.get_json(silent=True) or {}

#     email = data.get("email")

#     if not email:

#         return {
#             "success": False,
#             "message": "Email is required"
#         }, 400

#     user, error = AuthService.resend_verification_code(
#         email
#     )

#     if error:

#         return {
#             "success": False,
#             "message": error
#         }, 400

#     return {

#         "success": True,

#         "message": (
#             "A new verification code "
#             "has been sent to your email"
#         ),

#         "email": user.email

#     }, 200


# # ============================================================
# # LOGIN - STEP 1
# # ============================================================

# @auth_bp.post("/login")
# def login():

#     data = request.get_json(silent=True) or {}

#     valid, message = validate_login(data)

#     if not valid:

#         return {
#             "success": False,
#             "message": message
#         }, 400

#     user, error = AuthService.login(data)

#     if error:

#         return {
#             "success": False,
#             "message": error
#         }, 401

#     return {

#         "success": True,

#         "message": (
#             "Password verified. "
#             "A login verification code "
#             "has been sent to your email."
#         ),

#         "requires_otp": True,

#         "email": user.email

#     }, 200


# # ============================================================
# # VERIFY LOGIN OTP - STEP 2
# # ============================================================

# @auth_bp.post("/verify-login-otp")
# def verify_login_otp():

#     data = request.get_json(silent=True) or {}

#     email = data.get("email")
#     otp = data.get("otp")

#     if not email or not otp:

#         return {
#             "success": False,
#             "message": "Email and OTP are required"
#         }, 400

#     user, error = AuthService.verify_login_otp(
#         email,
#         otp
#     )

#     if error:

#         return {
#             "success": False,
#             "message": error
#         }, 401

#     # JWT is created ONLY after OTP verification
#     access_token = create_access_token(
#         identity=str(user.id)
#     )

#     return {

#         "success": True,

#         "message": "Login successful",

#         "access_token": access_token,

#         "user": {
#             "id": user.id,
#             "name": user.full_name,
#             "email": user.email,
#             "is_email_verified": user.is_email_verified
#         }

#     }, 200


# # ============================================================
# # RESEND LOGIN OTP
# # ============================================================

# @auth_bp.post("/resend-login-otp")
# def resend_login_otp():

#     data = request.get_json(silent=True) or {}

#     email = data.get("email")

#     if not email:

#         return {
#             "success": False,
#             "message": "Email is required"
#         }, 400

#     user, error = AuthService.resend_login_otp(
#         email
#     )

#     if error:

#         return {
#             "success": False,
#             "message": error
#         }, 400

#     return {

#         "success": True,

#         "message": (
#             "A new login verification code "
#             "has been sent to your email"
#         ),

#         "email": user.email

#     }, 200


# # ============================================================
# # CURRENT USER
# # ============================================================

# @auth_bp.get("/me")
# @jwt_required()
# def get_current_user():

#     user_id = get_jwt_identity()

#     user = AuthService.get_user_by_id(
#         user_id
#     )

#     if not user:

#         return {
#             "success": False,
#             "message": "User not found"
#         }, 404

#     return {

#         "success": True,

#         "user": {
#             "id": user.id,
#             "name": user.full_name,
#             "email": user.email,
#             "is_email_verified": user.is_email_verified
#         }

#     }, 200


# # ============================================================
# # FORGOT PASSWORD
# # ============================================================

# @auth_bp.post("/forgot-password")
# def forgot_password():

#     data = request.get_json(silent=True) or {}

#     email = data.get("email")

#     if not email:

#         return {
#             "success": False,
#             "message": "Email is required"
#         }, 400

#     success, message = AuthService.forgot_password(
#         email
#     )

#     return {
#         "success": success,
#         "message": message
#     }, 200


# # ============================================================
# # VERIFY PASSWORD RESET OTP
# # ============================================================

# @auth_bp.post("/verify-reset-otp")
# def verify_reset_otp():

#     data = request.get_json(silent=True) or {}

#     email = data.get("email")
#     otp = data.get("otp")

#     if not email or not otp:

#         return {
#             "success": False,
#             "message": "Email and OTP are required"
#         }, 400

#     user, error = AuthService.verify_reset_otp(
#         email,
#         otp
#     )

#     if error:

#         return {
#             "success": False,
#             "message": error
#         }, 400

#     return {
#         "success": True,
#         "message": "Password reset OTP verified successfully"
#     }, 200


# # ============================================================
# # RESET PASSWORD
# # ============================================================

# @auth_bp.post("/reset-password")
# def reset_password():

#     data = request.get_json(silent=True) or {}

#     email = data.get("email")
#     otp = data.get("otp")
#     new_password = data.get("new_password")

#     if not email or not otp or not new_password:

#         return {
#             "success": False,
#             "message": (
#                 "Email, OTP and new password are required"
#             )
#         }, 400

#     if len(new_password) < 8:

#         return {
#             "success": False,
#             "message": (
#                 "New password must be at least 8 characters"
#             )
#         }, 400

#     user, error = AuthService.reset_password(
#         email,
#         otp,
#         new_password
#     )

#     if error:

#         return {
#             "success": False,
#             "message": error
#         }, 400

#     return {
#         "success": True,
#         "message": "Password reset successfully",
#         "user": {
#             "id": user.id,
#             "name": user.full_name,
#             "email": user.email
#         }
#     }, 200


from flask import Blueprint, request

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from app.schemas.auth_schema import (
    validate_register,
    validate_login
)

from app.services.auth_service import AuthService


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


# ============================================================
# AUTH HOME
# ============================================================

@auth_bp.get("/")
def auth_home():

    return {
        "success": True,
        "message": "Authentication API is working"
    }


# ============================================================
# REGISTER
# ============================================================

@auth_bp.post("/register")
def register():

    data = request.get_json(silent=True) or {}

    valid, message = validate_register(data)

    if not valid:

        return {
            "success": False,
            "message": message
        }, 400

    user, error = AuthService.register(data)

    if error:

        return {
            "success": False,
            "message": error
        }, 409

    return {

        "success": True,

        "message": "Registration successful. You can now log in.",

        "user": {
            "id": user.id,
            "name": user.full_name,
            "email": user.email,
            "roles": [r.name for r in (user.roles or [])],
            "is_email_verified": True
        }

    }, 201


# ============================================================
# VERIFY EMAIL
# ============================================================

@auth_bp.post("/verify-email")
def verify_email():

    data = request.get_json(silent=True) or {}

    email = data.get("email")

    # Accept the new field name "verification_code".
    # Also accept "code" for backward compatibility.
    verification_code = data.get("verification_code") or data.get("code")

    if not email or not verification_code:

        return {
            "success": False,
            "message": "Email and verification code are required"
        }, 400

    user, error = AuthService.verify_email(
        email,
        verification_code
    )

    if error:

        return {
            "success": False,
            "message": error
        }, 400

    return {

        "success": True,

        "message": "Email verified successfully",

        "user": {
            "id": user.id,
            "name": user.full_name,
            "email": user.email,
            "roles": [r.name for r in (user.roles or [])],
            "hospital_id": getattr(user, "hospital_id", None),
            "is_email_verified": True
        }

    }, 200


# ============================================================
# RESEND EMAIL VERIFICATION
# ============================================================

@auth_bp.post("/resend-verification")
def resend_verification():

    data = request.get_json(silent=True) or {}

    email = data.get("email")

    if not email:

        return {
            "success": False,
            "message": "Email is required"
        }, 400

    user, error = AuthService.resend_verification_code(
        email
    )

    if error:

        return {
            "success": False,
            "message": error
        }, 400

    return {

        "success": True,

        "message": (
            "A new verification code "
            "has been sent to your email"
        ),

        "email": user.email

    }, 200


# ============================================================
# LOGIN - STEP 1
# ============================================================

@auth_bp.post("/login")
def login():

    data = request.get_json(silent=True) or {}

    valid, message = validate_login(data)

    if not valid:

        return {
            "success": False,
            "message": message
        }, 400

    user, error = AuthService.login(data)

    if error:

        return {
            "success": False,
            "message": error
        }, 401

    access_token = create_access_token(
        identity=str(user.id)
    )

    return {

        "success": True,

        "message": "Login successful",

        "access_token": access_token,

        "requires_otp": False,

        "user": {
            "id": user.id,
            "name": user.full_name,
            "email": user.email,
            "roles": [r.name for r in (user.roles or [])],
            "is_email_verified": True
        }

    }, 200


# ============================================================
# VERIFY LOGIN OTP - STEP 2
# ============================================================

@auth_bp.post("/verify-login-otp")
def verify_login_otp():

    data = request.get_json(silent=True) or {}

    email = data.get("email")
    otp = data.get("otp")

    if not email or not otp:

        return {
            "success": False,
            "message": "Email and OTP are required"
        }, 400

    user, error = AuthService.verify_login_otp(
        email,
        otp
    )

    if error:

        return {
            "success": False,
            "message": error
        }, 401

    # JWT is created ONLY after OTP verification
    access_token = create_access_token(
        identity=str(user.id)
    )

    return {

        "success": True,

        "message": "Login successful",

        "access_token": access_token,

        "user": {
            "id": user.id,
            "name": user.full_name,
            "email": user.email,
            "roles": [r.name for r in (user.roles or [])],
            "hospital_id": getattr(user, "hospital_id", None),
            "is_email_verified": True
        }

    }, 200


# ============================================================
# RESEND LOGIN OTP
# ============================================================

@auth_bp.post("/resend-login-otp")
def resend_login_otp():

    data = request.get_json(silent=True) or {}

    email = data.get("email")

    if not email:

        return {
            "success": False,
            "message": "Email is required"
        }, 400

    user, error, status_code = AuthService.resend_login_otp(
        email
    )

    if error:

        return {
            "success": False,
            "message": error
        }, status_code or 400

    return {

        "success": True,

        "message": (
            "A new login verification code "
            "has been sent to your email."
        ),

        "email": user.email

    }, 200


# ============================================================
# CURRENT USER
# ============================================================

@auth_bp.get("/me")
@jwt_required()
def get_current_user():

    user_id = get_jwt_identity()

    user = AuthService.get_user_by_id(
        user_id
    )

    if not user:

        return {
            "success": False,
            "message": "User not found"
        }, 404

    return {

        "success": True,

        "user": {
            "id": user.id,
            "name": user.full_name,
            "email": user.email,
            "roles": [r.name for r in (user.roles or [])],
            "hospital_id": getattr(user, "hospital_id", None),
            "is_email_verified": True
        }

    }, 200


# ============================================================
# FORGOT PASSWORD
# ============================================================

@auth_bp.post("/forgot-password")
def forgot_password():

    data = request.get_json(silent=True) or {}

    email = data.get("email")

    if not email:

        return {
            "success": False,
            "message": "Email is required"
        }, 400

    success, message = AuthService.forgot_password(
        email
    )

    return {
        "success": success,
        "message": message
    }, 200


# ============================================================
# VERIFY PASSWORD RESET OTP
# ============================================================

@auth_bp.post("/verify-reset-otp")
def verify_reset_otp():

    data = request.get_json(silent=True) or {}

    email = data.get("email")
    otp = data.get("otp")

    if not email or not otp:

        return {
            "success": False,
            "message": "Email and OTP are required"
        }, 400

    user, error = AuthService.verify_reset_otp(
        email,
        otp
    )

    if error:

        return {
            "success": False,
            "message": error
        }, 400

    return {
        "success": True,
        "message": "Password reset OTP verified successfully"
    }, 200


# ============================================================
# RESET PASSWORD
# ============================================================

@auth_bp.post("/reset-password")
def reset_password():

    data = request.get_json(silent=True) or {}

    email = data.get("email")
    otp = data.get("otp")
    new_password = data.get("new_password")

    if not email or not otp or not new_password:

        return {
            "success": False,
            "message": (
                "Email, OTP and new password are required"
            )
        }, 400

    if len(new_password) < 8:

        return {
            "success": False,
            "message": (
                "New password must be at least 8 characters"
            )
        }, 400

    user, error = AuthService.reset_password(
        email,
        otp,
        new_password
    )

    if error:

        return {
            "success": False,
            "message": error
        }, 400

    return {
        "success": True,
        "message": "Password reset successfully",
        "user": {
            "id": user.id,
            "name": user.full_name,
            "email": user.email
        }
    }, 200