from datetime import datetime


# =========================================================
# APPOINTMENT VALIDATOR
# =========================================================

def validate_appointment(data):

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
        "hospital_id",
        "appointment_date",
        "appointment_time"
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

        if isinstance(data[field], str):

            if not data[field].strip():

                return (
                    False,
                    f"{field} cannot be empty"
                )

    # =====================================================
    # ID VALIDATION
    # =====================================================

    id_fields = [
        "patient_id",
        "doctor_id",
        "hospital_id"
    ]

    for field in id_fields:

        try:

            value = int(data[field])

            if value <= 0:

                return (
                    False,
                    f"{field} must be a valid positive number"
                )

        except (ValueError, TypeError):

            return (
                False,
                f"{field} must be a valid number"
            )

    # =====================================================
    # DATE VALIDATION
    # =====================================================

    try:

        appointment_date = datetime.strptime(
            str(data["appointment_date"]).strip(),
            "%Y-%m-%d"
        ).date()

    except (ValueError, TypeError):

        return (
            False,
            "appointment_date must be in YYYY-MM-DD format"
        )

    # -----------------------------------------------------
    # Prevent appointments in the past
    # -----------------------------------------------------

    from datetime import date

    if appointment_date < date.today():

        return (
            False,
            "Appointment date cannot be in the past"
        )

    # =====================================================
    # TIME VALIDATION
    # =====================================================

    appointment_time = None

    time_value = str(
        data["appointment_time"]
    ).strip()

    for time_format in (
        "%H:%M",
        "%H:%M:%S"
    ):

        try:

            appointment_time = datetime.strptime(
                time_value,
                time_format
            ).time()

            break

        except ValueError:

            continue

    if appointment_time is None:

        return (
            False,
            "appointment_time must be in HH:MM or HH:MM:SS format"
        )

    # =====================================================
    # STATUS VALIDATION
    # =====================================================

    valid_statuses = [
        "Pending",
        "Confirmed",
        "Cancelled",
        "Completed",
        "No Show"
    ]

    if "status" in data:

        if data["status"] is not None:

            status = str(
                data["status"]
            ).strip()

            matched_status = None

            for valid_status in valid_statuses:

                if status.lower() == valid_status.lower():

                    matched_status = valid_status

                    break

            if matched_status is None:

                return (
                    False,
                    "Invalid appointment status"
                )

    # =====================================================
    # CONSULTATION MODE
    # =====================================================

    valid_consultation_modes = [
        "Offline",
        "Online"
    ]

    if "consultation_mode" in data:

        if data["consultation_mode"] is not None:

            mode = str(
                data["consultation_mode"]
            ).strip()

            matched_mode = None

            for valid_mode in valid_consultation_modes:

                if mode.lower() == valid_mode.lower():

                    matched_mode = valid_mode

                    break

            if matched_mode is None:

                return (
                    False,
                    "consultation_mode must be Offline or Online"
                )

    # =====================================================
    # PAYMENT STATUS
    # =====================================================

    valid_payment_statuses = [
        "Pending",
        "Paid",
        "Failed",
        "Refunded"
    ]

    if "payment_status" in data:

        if data["payment_status"] is not None:

            payment_status = str(
                data["payment_status"]
            ).strip()

            matched_payment_status = None

            for valid_status in valid_payment_statuses:

                if (
                    payment_status.lower()
                    == valid_status.lower()
                ):

                    matched_payment_status = valid_status

                    break

            if matched_payment_status is None:

                return (
                    False,
                    "Invalid payment_status"
                )

    # =====================================================
    # VALIDATION SUCCESSFUL
    # =====================================================

    return True, ""


# =========================================================
# APPOINTMENT → DICTIONARY
# =========================================================

def appointment_to_dict(appointment):

    return {

        "id": appointment.id,

        # -------------------------------------------------
        # Relationships
        # -------------------------------------------------

        "patient_id": appointment.patient_id,

        "doctor_id": appointment.doctor_id,

        "hospital_id": appointment.hospital_id,

        # -------------------------------------------------
        # Appointment date
        # -------------------------------------------------

        "appointment_date": (
            appointment.appointment_date.strftime(
                "%Y-%m-%d"
            )
            if appointment.appointment_date
            else None
        ),

        # -------------------------------------------------
        # Appointment time
        # -------------------------------------------------

        "appointment_time": (
            appointment.appointment_time.strftime(
                "%H:%M:%S"
            )
            if appointment.appointment_time
            else None
        ),

        # -------------------------------------------------
        # Appointment information
        # -------------------------------------------------

        "reason": appointment.reason,

        "status": appointment.status,

        "consultation_mode": (
            appointment.consultation_mode
        ),

        "payment_status": (
            appointment.payment_status
        ),

        "notes": appointment.notes,

        # -------------------------------------------------
        # Timestamps
        # -------------------------------------------------

        "created_at": (
            appointment.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if appointment.created_at
            else None
        ),

        "updated_at": (
            appointment.updated_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if appointment.updated_at
            else None
        )
    }