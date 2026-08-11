# =========================================================
# HOSPITAL SCHEMA
# =========================================================


def validate_hospital(data):

    # -----------------------------------------------------
    # Check request body
    # -----------------------------------------------------

    if not data:
        return False, "Request body is required"

    # -----------------------------------------------------
    # Required fields
    # -----------------------------------------------------

    required_fields = [
        "name",
        "registration_number",
        "hospital_type",
        "email",
        "phone",
        "address",
        "city",
        "state",
        "pincode"
    ]

    for field in required_fields:

        if field not in data:
            return False, f"{field} is required"

        if data[field] is None:
            return False, f"{field} is required"

        if isinstance(data[field], str) and not data[field].strip():
            return False, f"{field} cannot be empty"

    # -----------------------------------------------------
    # Email validation
    # -----------------------------------------------------

    email = data["email"].strip()

    if "@" not in email or "." not in email:
        return False, "Invalid email address"

    # -----------------------------------------------------
    # Phone validation
    # -----------------------------------------------------

    phone = str(data["phone"]).strip()

    if len(phone) < 10:
        return False, "Invalid phone number"

    # -----------------------------------------------------
    # Pincode validation
    # -----------------------------------------------------

    pincode = str(data["pincode"]).strip()

    if len(pincode) < 4:
        return False, "Invalid pincode"

    # -----------------------------------------------------
    # Numeric validation
    # -----------------------------------------------------

    numeric_fields = [
        "total_beds",
        "icu_beds",
        "emergency_beds",
        "operation_theatres"
    ]

    for field in numeric_fields:

        if field in data and data[field] is not None:

            try:
                value = int(data[field])

                if value < 0:
                    return False, f"{field} cannot be negative"

            except (ValueError, TypeError):

                return False, f"{field} must be a valid number"

    # -----------------------------------------------------
    # Latitude validation
    # -----------------------------------------------------

    if data.get("latitude") is not None:

        try:
            latitude = float(data["latitude"])

            if latitude < -90 or latitude > 90:
                return False, "Latitude must be between -90 and 90"

        except (ValueError, TypeError):

            return False, "Invalid latitude"

    # -----------------------------------------------------
    # Longitude validation
    # -----------------------------------------------------

    if data.get("longitude") is not None:

        try:
            longitude = float(data["longitude"])

            if longitude < -180 or longitude > 180:
                return False, "Longitude must be between -180 and 180"

        except (ValueError, TypeError):

            return False, "Invalid longitude"

    # -----------------------------------------------------
    # Boolean validation
    # -----------------------------------------------------

    boolean_fields = [
        "is_24x7",
        "is_verified",
        "is_active"
    ]

    for field in boolean_fields:

        if field in data and data[field] is not None:

            if not isinstance(data[field], bool):
                return False, f"{field} must be true or false"

    # -----------------------------------------------------
    # Validation successful
    # -----------------------------------------------------

    return True, None


# =========================================================
# HOSPITAL → DICTIONARY
# =========================================================


def hospital_to_dict(hospital):

    return {

        # -------------------------------------------------
        # Basic Information
        # -------------------------------------------------

        "id": hospital.id,
        "name": hospital.name,
        "registration_number": hospital.registration_number,
        "hospital_type": hospital.hospital_type,
        "description": hospital.description,

        # -------------------------------------------------
        # Contact Information
        # -------------------------------------------------

        "email": hospital.email,
        "phone": hospital.phone,
        "emergency_contact": hospital.emergency_contact,
        "website": hospital.website,

        # -------------------------------------------------
        # Address
        # -------------------------------------------------

        "address": hospital.address,
        "city": hospital.city,
        "state": hospital.state,
        "pincode": hospital.pincode,

        # -------------------------------------------------
        # Location
        # -------------------------------------------------

        "latitude": hospital.latitude,
        "longitude": hospital.longitude,

        # -------------------------------------------------
        # Hospital Capacity
        # -------------------------------------------------

        "total_beds": hospital.total_beds,
        "icu_beds": hospital.icu_beds,
        "emergency_beds": hospital.emergency_beds,
        "operation_theatres": hospital.operation_theatres,

        # -------------------------------------------------
        # Working Hours
        # -------------------------------------------------

        "opening_time": hospital.opening_time,
        "closing_time": hospital.closing_time,
        "is_24x7": hospital.is_24x7,

        # -------------------------------------------------
        # Media
        # -------------------------------------------------

        "logo": hospital.logo,
        "banner": hospital.banner,

        # -------------------------------------------------
        # Status
        # -------------------------------------------------

        "is_verified": hospital.is_verified,
        "is_active": hospital.is_active,

        # -------------------------------------------------
        # Hospital Owner / User
        # -------------------------------------------------

        "user_id": hospital.user_id,

        # -------------------------------------------------
        # Timestamps
        # -------------------------------------------------

        "created_at": hospital.created_at,
        "updated_at": hospital.updated_at
    }