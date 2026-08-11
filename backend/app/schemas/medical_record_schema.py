# =========================================================
# MEDICAL RECORD SCHEMA
# =========================================================


def validate_medical_record(data):

    # -----------------------------------------------------
    # Check request body
    # -----------------------------------------------------

    if not data:

        return (
            False,
            "Request body is required"
        )

    # -----------------------------------------------------
    # Required fields
    # -----------------------------------------------------

    required_fields = [
        "patient_id",
        "doctor_id",
        "diagnosis"
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

        if (
            isinstance(data[field], str)
            and not data[field].strip()
        ):

            return (
                False,
                f"{field} cannot be empty"
            )

    # -----------------------------------------------------
    # Patient ID validation
    # -----------------------------------------------------

    try:

        patient_id = int(
            data["patient_id"]
        )

        if patient_id <= 0:

            return (
                False,
                "patient_id must be a valid positive number"
            )

    except (ValueError, TypeError):

        return (
            False,
            "patient_id must be a valid number"
        )

    # -----------------------------------------------------
    # Doctor ID validation
    # -----------------------------------------------------

    try:

        doctor_id = int(
            data["doctor_id"]
        )

        if doctor_id <= 0:

            return (
                False,
                "doctor_id must be a valid positive number"
            )

    except (ValueError, TypeError):

        return (
            False,
            "doctor_id must be a valid number"
        )

    # -----------------------------------------------------
    # Appointment ID validation
    # -----------------------------------------------------

    if data.get("appointment_id") is not None:

        try:

            appointment_id = int(
                data["appointment_id"]
            )

            if appointment_id <= 0:

                return (
                    False,
                    "appointment_id must be a valid positive number"
                )

        except (ValueError, TypeError):

            return (
                False,
                "appointment_id must be a valid number"
            )

    # -----------------------------------------------------
    # Diagnosis validation
    # -----------------------------------------------------

    if not isinstance(
        data["diagnosis"],
        str
    ):

        return (
            False,
            "diagnosis must be a text value"
        )

    if not data["diagnosis"].strip():

        return (
            False,
            "diagnosis cannot be empty"
        )

    # -----------------------------------------------------
    # Follow-up date validation
    # -----------------------------------------------------

    if data.get("follow_up_date"):

        if not isinstance(
            data["follow_up_date"],
            str
        ):

            return (
                False,
                "follow_up_date must be in YYYY-MM-DD format"
            )

        parts = data[
            "follow_up_date"
        ].split("-")

        if len(parts) != 3:

            return (
                False,
                "follow_up_date must be in YYYY-MM-DD format"
            )

        try:

            year = int(parts[0])
            month = int(parts[1])
            day = int(parts[2])

            if (
                year < 1900
                or month < 1
                or month > 12
                or day < 1
                or day > 31
            ):

                return (
                    False,
                    "follow_up_date must be a valid date"
                )

        except (ValueError, TypeError):

            return (
                False,
                "follow_up_date must be in YYYY-MM-DD format"
            )

    # -----------------------------------------------------
    # Validation successful
    # -----------------------------------------------------

    return True, None


# =========================================================
# MEDICAL RECORD SERIALIZER
# =========================================================


def medical_record_to_dict(record):

    return {

        "id": record.id,

        "patient_id": record.patient_id,

        "doctor_id": record.doctor_id,

        "appointment_id": record.appointment_id,

        "diagnosis": record.diagnosis,

        "symptoms": record.symptoms,

        "prescription": record.prescription,

        "lab_tests": record.lab_tests,

        "notes": record.notes,

        "follow_up_date": (
            record.follow_up_date.strftime(
                "%Y-%m-%d"
            )
            if record.follow_up_date
            else None
        ),

        "created_at": (
            record.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if record.created_at
            else None
        ),

        "updated_at": (
            record.updated_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if record.updated_at
            else None
        )
    }