# backend/app/schemas/patient_schema.py

from datetime import datetime, date
import re


# =========================================================
# PATIENT VALIDATOR
# =========================================================

def validate_patient(data):

    # -----------------------------------------------------
    # Check request body
    # -----------------------------------------------------

    if not data:
        return False, "Request body is required"

    # -----------------------------------------------------
    # Required fields
    # -----------------------------------------------------

    required_fields = [
        "full_name",
        "email",
        "phone",
        "gender",
        "date_of_birth"
    ]

    for field in required_fields:

        if field not in data:
            return False, f"{field} is required"

        if data[field] is None:
            return False, f"{field} is required"

        if isinstance(data[field], str) and not data[field].strip():
            return False, f"{field} cannot be empty"

    # -----------------------------------------------------
    # Full name validation
    # -----------------------------------------------------

    full_name = str(data["full_name"]).strip()

    if len(full_name) < 2:
        return False, "full_name must contain at least 2 characters"

    if len(full_name) > 255:
        return False, "full_name cannot exceed 255 characters"

    # -----------------------------------------------------
    # Email validation
    # -----------------------------------------------------

    email = str(data["email"]).strip().lower()

    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.match(email_pattern, email):
        return False, "Invalid email address"

    # -----------------------------------------------------
    # Phone validation
    # -----------------------------------------------------

    phone = str(data["phone"]).strip()

    phone_digits = re.sub(r"\D", "", phone)

    if len(phone_digits) < 10:
        return False, "Invalid phone number"

    if len(phone_digits) > 15:
        return False, "Invalid phone number"

    # -----------------------------------------------------
    # Gender validation
    # -----------------------------------------------------

    gender = str(data["gender"]).strip().lower()

    valid_genders = [
        "male",
        "female",
        "other"
    ]

    if gender not in valid_genders:
        return (
            False,
            "gender must be Male, Female, or Other"
        )

    # -----------------------------------------------------
    # Date of birth validation
    # -----------------------------------------------------

    dob = data["date_of_birth"]

    if isinstance(dob, date):
        date_of_birth = dob

    elif isinstance(dob, str):

        try:
            date_of_birth = datetime.strptime(
                dob.strip(),
                "%Y-%m-%d"
            ).date()

        except ValueError:

            return (
                False,
                "date_of_birth must be in YYYY-MM-DD format"
            )

    else:

        return (
            False,
            "date_of_birth must be in YYYY-MM-DD format"
        )

    # DOB cannot be in the future

    if date_of_birth > date.today():

        return (
            False,
            "date_of_birth cannot be in the future"
        )

    # -----------------------------------------------------
    # Blood group validation
    # -----------------------------------------------------

    if data.get("blood_group"):

        blood_group = str(
            data["blood_group"]
        ).strip().upper()

        valid_blood_groups = [
            "A+",
            "A-",
            "B+",
            "B-",
            "AB+",
            "AB-",
            "O+",
            "O-"
        ]

        if blood_group not in valid_blood_groups:

            return (
                False,
                "Invalid blood_group"
            )

    # -----------------------------------------------------
    # Pincode validation
    # -----------------------------------------------------

    if data.get("pincode"):

        pincode = str(
            data["pincode"]
        ).strip()

        if not pincode.isdigit():

            return (
                False,
                "pincode must contain only numbers"
            )

        if len(pincode) < 4 or len(pincode) > 10:

            return (
                False,
                "Invalid pincode"
            )

    # -----------------------------------------------------
    # Emergency contact phone validation
    # -----------------------------------------------------

    if data.get("emergency_contact_phone"):

        emergency_phone = str(
            data["emergency_contact_phone"]
        ).strip()

        emergency_digits = re.sub(
            r"\D",
            "",
            emergency_phone
        )

        if (
            len(emergency_digits) < 10
            or len(emergency_digits) > 15
        ):

            return (
                False,
                "Invalid emergency contact phone number"
            )

    # -----------------------------------------------------
    # Insurance date validation
    # -----------------------------------------------------

    if data.get("insurance_valid_until"):

        insurance_date = data[
            "insurance_valid_until"
        ]

        if isinstance(
            insurance_date,
            date
        ):

            pass

        elif isinstance(
            insurance_date,
            str
        ):

            try:

                datetime.strptime(
                    insurance_date.strip(),
                    "%Y-%m-%d"
                ).date()

            except ValueError:

                return (
                    False,
                    "insurance_valid_until must be in YYYY-MM-DD format"
                )

        else:

            return (
                False,
                "insurance_valid_until must be in YYYY-MM-DD format"
            )

    # -----------------------------------------------------
    # User ID validation
    # -----------------------------------------------------

    if data.get("user_id") is not None:

        try:

            user_id = int(
                data["user_id"]
            )

            if user_id <= 0:

                return (
                    False,
                    "user_id must be a valid positive number"
                )

        except (
            ValueError,
            TypeError
        ):

            return (
                False,
                "user_id must be a valid number"
            )

    # -----------------------------------------------------
    # Active validation
    # -----------------------------------------------------

    if data.get("active") is not None:

        if not isinstance(
            data["active"],
            bool
        ):

            return (
                False,
                "active must be true or false"
            )

    # -----------------------------------------------------
    # Verified validation
    # -----------------------------------------------------

    if data.get("is_verified") is not None:

        if not isinstance(
            data["is_verified"],
            bool
        ):

            return (
                False,
                "is_verified must be true or false"
            )

    # -----------------------------------------------------
    # Validation successful
    # -----------------------------------------------------

    return True, ""


# =========================================================
# PATIENT → DICTIONARY
# =========================================================

def patient_to_dict(patient):

    return {

        # -------------------------------------------------
        # Basic information
        # -------------------------------------------------

        "id": patient.id,

        "full_name": patient.full_name,

        "email": patient.email,

        "phone": patient.phone,

        "gender": patient.gender,

        "date_of_birth": (
            patient.date_of_birth.strftime("%Y-%m-%d")
            if patient.date_of_birth
            else None
        ),

        "age": patient.age,

        # -------------------------------------------------
        # Medical information
        # -------------------------------------------------

        "blood_group": patient.blood_group,

        "allergies": patient.allergies,

        "chronic_conditions": (
            patient.chronic_conditions
        ),

        "current_medications": (
            patient.current_medications
        ),

        "medical_history": (
            patient.medical_history
        ),

        # -------------------------------------------------
        # Address
        # -------------------------------------------------

        "address": patient.address,

        "city": patient.city,

        "state": patient.state,

        "pincode": patient.pincode,

        "country": patient.country,

        # -------------------------------------------------
        # Emergency contact
        # -------------------------------------------------

        "emergency_contact_name": (
            patient.emergency_contact_name
        ),

        "emergency_contact_phone": (
            patient.emergency_contact_phone
        ),

        "emergency_contact_relation": (
            patient.emergency_contact_relation
        ),

        # -------------------------------------------------
        # Profile
        # -------------------------------------------------

        "profile_photo": patient.profile_photo,

        "active": patient.active,

        "is_verified": patient.is_verified,

        # -------------------------------------------------
        # Insurance
        # -------------------------------------------------

        "insurance_provider": (
            patient.insurance_provider
        ),

        "insurance_policy_number": (
            patient.insurance_policy_number
        ),

        "insurance_valid_until": (
            patient.insurance_valid_until.strftime(
                "%Y-%m-%d"
            )
            if patient.insurance_valid_until
            else None
        ),

        # -------------------------------------------------
        # User relationship
        # -------------------------------------------------

        "user_id": patient.user_id,

        # -------------------------------------------------
        # Timestamps
        # -------------------------------------------------

        "created_at": (
            patient.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if patient.created_at
            else None
        ),

        "updated_at": (
            patient.updated_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if patient.updated_at
            else None
        )
    }