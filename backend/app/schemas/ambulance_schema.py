# =========================================================
# MEDILINK AMBULANCE SCHEMA
# =========================================================


# =========================================================
# VALIDATE AMBULANCE
# =========================================================

def validate_ambulance(data):

    required_fields = [
        "hospital_id",
        "registration_number",
        "ambulance_type",
        "driver_name",
        "driver_phone"
    ]

    # =====================================================
    # REQUIRED FIELDS
    # =====================================================

    for field in required_fields:

        if field not in data or data[field] in (None, ""):

            return False, f"{field} is required"

    # =====================================================
    # HOSPITAL ID VALIDATION
    # =====================================================

    try:

        hospital_id = int(
            data["hospital_id"]
        )

        if hospital_id <= 0:

            return (
                False,
                "hospital_id must be a valid positive integer"
            )

    except (TypeError, ValueError):

        return (
            False,
            "hospital_id must be a valid integer"
        )

    # =====================================================
    # REGISTRATION NUMBER VALIDATION
    # =====================================================

    if not isinstance(
        data["registration_number"],
        str
    ):

        return (
            False,
            "registration_number must be a string"
        )

    if len(
        data["registration_number"].strip()
    ) > 100:

        return (
            False,
            "registration_number cannot exceed 100 characters"
        )

    # =====================================================
    # AMBULANCE TYPE VALIDATION
    # =====================================================

    if not isinstance(
        data["ambulance_type"],
        str
    ):

        return (
            False,
            "ambulance_type must be a string"
        )

    if len(
        data["ambulance_type"].strip()
    ) > 100:

        return (
            False,
            "ambulance_type cannot exceed 100 characters"
        )

    # =====================================================
    # DRIVER NAME VALIDATION
    # =====================================================

    if not isinstance(
        data["driver_name"],
        str
    ):

        return (
            False,
            "driver_name must be a string"
        )

    if len(
        data["driver_name"].strip()
    ) > 150:

        return (
            False,
            "driver_name cannot exceed 150 characters"
        )

    # =====================================================
    # DRIVER PHONE VALIDATION
    # =====================================================

    if not isinstance(
        data["driver_phone"],
        str
    ):

        return (
            False,
            "driver_phone must be a string"
        )

    if len(
        data["driver_phone"].strip()
    ) > 20:

        return (
            False,
            "driver_phone cannot exceed 20 characters"
        )

    # =====================================================
    # CURRENT LOCATION VALIDATION
    # =====================================================

    if "current_location" in data:

        if (
            data["current_location"] is not None
            and not isinstance(
                data["current_location"],
                str
            )
        ):

            return (
                False,
                "current_location must be a string"
            )

    # =====================================================
    # AVAILABILITY STATUS VALIDATION
    # =====================================================

    if "availability_status" in data:

        allowed_statuses = [
            "Available",
            "Busy",
            "Maintenance",
            "Unavailable"
        ]

        if data["availability_status"] not in allowed_statuses:

            return (
                False,
                "availability_status must be Available, Busy, Maintenance, or Unavailable"
            )

    # =====================================================
    # EMERGENCY STATUS VALIDATION
    # =====================================================

    if "emergency_status" in data:

        allowed_statuses = [
            "Normal",
            "Emergency"
        ]

        if data["emergency_status"] not in allowed_statuses:

            return (
                False,
                "emergency_status must be Normal or Emergency"
            )

    # =====================================================
    # VALID
    # =====================================================

    return True, ""


# =========================================================
# AMBULANCE TO DICT
# =========================================================

def ambulance_to_dict(ambulance):

    return {

        "id": ambulance.id,

        "hospital_id": ambulance.hospital_id,

        "registration_number": (
            ambulance.registration_number
        ),

        "ambulance_type": (
            ambulance.ambulance_type
        ),

        "driver_name": (
            ambulance.driver_name
        ),

        "driver_phone": (
            ambulance.driver_phone
        ),

        "current_location": (
            ambulance.current_location
        ),

        "availability_status": (
            ambulance.availability_status
        ),

        "emergency_status": (
            ambulance.emergency_status
        ),

        "created_at": (
            ambulance.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if ambulance.created_at
            else None
        ),

        "updated_at": (
            ambulance.updated_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if ambulance.updated_at
            else None
        )
    }