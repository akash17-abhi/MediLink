# =========================================================
# PATIENT VALIDATOR
# =========================================================

from datetime import datetime


def validate_patient(data):

    # =====================================================
    # REQUEST BODY
    # =====================================================

    if not data:
        return False, "Request body is required"

    # =====================================================
    # REQUIRED FIELDS
    # =====================================================

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

        if (
            isinstance(data[field], str)
            and not data[field].strip()
        ):
            return False, f"{field} cannot be empty"

    # =====================================================
    # FULL NAME
    # =====================================================

    full_name = str(
        data["full_name"]
    ).strip()

    if len(full_name) < 2:

        return (
            False,
            "full_name must contain at least 2 characters"
        )

    if len(full_name) > 255:

        return (
            False,
            "full_name cannot exceed 255 characters"
        )

    # =====================================================
    # EMAIL
    # =====================================================

    email = str(
        data["email"]
    ).strip()

    if (
        "@" not in email
        or "." not in email.split("@")[-1]
    ):

        return False, "Invalid email address"

    # =====================================================
    # PHONE
    # =====================================================

    phone = str(
        data["phone"]
    ).strip()

    if not phone.isdigit():

        return False, "Phone number must contain digits only"

    if len(phone) < 10 or len(phone) > 15:

        return (
            False,
            "Phone number must contain 10 to 15 digits"
        )

    # =====================================================
    # GENDER
    # =====================================================

    gender = str(
        data["gender"]
    ).strip().capitalize()

    valid_genders = [
        "Male",
        "Female",
        "Other"
    ]

    if gender not in valid_genders:

        return (
            False,
            "gender must be Male, Female, or Other"
        )

    # =====================================================
    # DATE OF BIRTH
    # =====================================================

    date_of_birth = data["date_of_birth"]

    if not isinstance(
        date_of_birth,
        str
    ):

        return (
            False,
            "date_of_birth must be in YYYY-MM-DD format"
        )

    try:

        dob = datetime.strptime(
            date_of_birth,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        return (
            False,
            "date_of_birth must be in YYYY-MM-DD format"
        )

    # DOB cannot be in the future

    from datetime import date

    if dob > date.today():

        return (
            False,
            "date_of_birth cannot be in the future"
        )

    # =====================================================
    # BLOOD GROUP
    # =====================================================

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

    # =====================================================
    # ADDRESS
    # =====================================================

    if data.get("address"):

        if len(
            str(data["address"]).strip()
        ) > 10000:

            return (
                False,
                "address is too long"
            )

    # =====================================================
    # CITY
    # =====================================================

    if data.get("city"):

        if len(
            str(data["city"]).strip()
        ) > 100:

            return (
                False,
                "city cannot exceed 100 characters"
            )

    # =====================================================
    # STATE
    # =====================================================

    if data.get("state"):

        if len(
            str(data["state"]).strip()
        ) > 100:

            return (
                False,
                "state cannot exceed 100 characters"
            )

    # =====================================================
    # PINCODE
    # =====================================================

    if data.get("pincode"):

        pincode = str(
            data["pincode"]
        ).strip()

        if not pincode.isdigit():

            return (
                False,
                "pincode must contain digits only"
            )

        if len(pincode) < 4 or len(pincode) > 10:

            return (
                False,
                "Invalid pincode"
            )

    # =====================================================
    # EMERGENCY CONTACT PHONE
    # =====================================================

    if data.get("emergency_contact_phone"):

        emergency_phone = str(
            data["emergency_contact_phone"]
        ).strip()

        if not emergency_phone.isdigit():

            return (
                False,
                "Emergency contact phone must contain digits only"
            )

        if (
            len(emergency_phone) < 10
            or len(emergency_phone) > 15
        ):

            return (
                False,
                "Invalid emergency contact phone"
            )

    # =====================================================
    # INSURANCE VALID UNTIL
    # =====================================================

    if data.get("insurance_valid_until"):

        insurance_date = data[
            "insurance_valid_until"
        ]

        if not isinstance(
            insurance_date,
            str
        ):

            return (
                False,
                "insurance_valid_until must be in YYYY-MM-DD format"
            )

        try:

            datetime.strptime(
                insurance_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            return (
                False,
                "insurance_valid_until must be in YYYY-MM-DD format"
            )

    # =====================================================
    # PROFILE PHOTO
    # =====================================================

    if data.get("profile_photo"):

        if len(
            str(data["profile_photo"])
        ) > 500:

            return (
                False,
                "profile_photo cannot exceed 500 characters"
            )

    # =====================================================
    # ACTIVE
    # =====================================================

    if "active" in data:

        if data["active"] is not None:

            if not isinstance(
                data["active"],
                bool
            ):

                return (
                    False,
                    "active must be true or false"
                )

    # =====================================================
    # VERIFIED
    # =====================================================

    if "is_verified" in data:

        if data["is_verified"] is not None:

            if not isinstance(
                data["is_verified"],
                bool
            ):

                return (
                    False,
                    "is_verified must be true or false"
                )

    # =====================================================
    # USER ID
    # =====================================================

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

    # =====================================================
    # VALIDATION SUCCESSFUL
    # =====================================================

    return True, None