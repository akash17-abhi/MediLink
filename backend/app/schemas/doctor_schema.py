# =========================================================
# DOCTOR VALIDATOR
# =========================================================

def validate_doctor(data):

    # -----------------------------------------------------
    # Check request body
    # -----------------------------------------------------

    if not data:
        return False, "Request body is required"


    # -----------------------------------------------------
    # Required fields
    # -----------------------------------------------------

    required_fields = [
        "hospital_id",
        "full_name",
        "email",
        "phone",
        "specialization"
    ]


    for field in required_fields:

        if field not in data:

            return (
                False,
                f"{field} is required"
            )

        if data[field] is None:

            return (
                False,
                f"{field} is required"
            )

        if isinstance(
            data[field],
            str
        ) and not data[field].strip():

            return (
                False,
                f"{field} cannot be empty"
            )


    # -----------------------------------------------------
    # Hospital ID validation
    # -----------------------------------------------------

    try:

        hospital_id = int(
            data["hospital_id"]
        )

        if hospital_id <= 0:

            return (
                False,
                "hospital_id must be a valid positive number"
            )

    except (
        ValueError,
        TypeError
    ):

        return (
            False,
            "hospital_id must be a valid number"
        )


    # -----------------------------------------------------
    # Email validation
    # -----------------------------------------------------

    email = str(
        data["email"]
    ).strip()

    if (
        "@" not in email
        or "." not in email.split("@")[-1]
    ):

        return (
            False,
            "Invalid email address"
        )


    # -----------------------------------------------------
    # Phone validation
    # -----------------------------------------------------

    phone = str(
        data["phone"]
    ).strip()

    if len(phone) < 10:

        return (
            False,
            "Invalid phone number"
        )


    # -----------------------------------------------------
    # Experience validation
    # -----------------------------------------------------

    if data.get("experience") is not None:

        try:

            experience = int(
                data["experience"]
            )

            if experience < 0:

                return (
                    False,
                    "experience cannot be negative"
                )

        except (
            ValueError,
            TypeError
        ):

            return (
                False,
                "experience must be a valid number"
            )


    # -----------------------------------------------------
    # Consultation fee validation
    # -----------------------------------------------------

    if data.get("consultation_fee") is not None:

        try:

            consultation_fee = float(
                data["consultation_fee"]
            )

            if consultation_fee < 0:

                return (
                    False,
                    "consultation_fee cannot be negative"
                )

        except (
            ValueError,
            TypeError
        ):

            return (
                False,
                "consultation_fee must be a valid number"
            )


    # -----------------------------------------------------
    # is_active validation
    # -----------------------------------------------------

    if data.get("is_active") is not None:

        if not isinstance(
            data["is_active"],
            bool
        ):

            return (
                False,
                "is_active must be true or false"
            )


    # -----------------------------------------------------
    # Validation successful
    # -----------------------------------------------------

    return True, None


# =========================================================
# DOCTOR → DICTIONARY
# =========================================================

def doctor_to_dict(doctor):

    return {

        "id": doctor.id,

        "full_name": doctor.full_name,

        "email": doctor.email,

        "phone": doctor.phone,

        "specialization": doctor.specialization,

        "qualification": doctor.qualification,

        "experience": doctor.experience,

        "consultation_fee": doctor.consultation_fee,

        "profile_photo": doctor.profile_photo,

        "hospital_id": doctor.hospital_id,

        "is_active": doctor.is_active,

        "created_at": doctor.created_at,

        "updated_at": doctor.updated_at
    }