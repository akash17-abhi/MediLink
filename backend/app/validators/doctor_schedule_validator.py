# =========================================================
# DOCTOR SCHEDULE VALIDATOR
# =========================================================


def validate_doctor_schedule(data):

    # -----------------------------------------------------
    # Check request body
    # -----------------------------------------------------

    if not data:
        return False, "Request body is required"

    # -----------------------------------------------------
    # Required fields
    # -----------------------------------------------------

    required_fields = [
        "doctor_id",
        "day_of_week",
        "start_time",
        "end_time"
    ]

    for field in required_fields:

        if field not in data:
            return False, f"{field} is required"

        if data[field] is None:
            return False, f"{field} is required"

        if isinstance(data[field], str) and not data[field].strip():
            return False, f"{field} cannot be empty"

    # -----------------------------------------------------
    # Doctor ID validation
    # -----------------------------------------------------

    try:
        doctor_id = int(data["doctor_id"])

        if doctor_id <= 0:
            return False, "doctor_id must be a valid positive number"

    except (ValueError, TypeError):

        return False, "doctor_id must be a valid number"

    # -----------------------------------------------------
    # Day of week validation
    # -----------------------------------------------------

    valid_days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    day = str(data["day_of_week"]).strip().capitalize()

    if day not in valid_days:
        return (
            False,
            "day_of_week must be a valid day of the week"
        )

    # -----------------------------------------------------
    # Time validation
    # -----------------------------------------------------

    def validate_time(value, field_name):

        if not isinstance(value, str):
            return False

        value = value.strip()

        parts = value.split(":")

        if len(parts) != 2:
            return False

        try:
            hour = int(parts[0])
            minute = int(parts[1])

        except ValueError:
            return False

        if hour < 0 or hour > 23:
            return False

        if minute < 0 or minute > 59:
            return False

        return True

    # -----------------------------------------------------
    # Start time
    # -----------------------------------------------------

    if not validate_time(
        data["start_time"],
        "start_time"
    ):
        return False, "start_time must be in HH:MM format"

    # -----------------------------------------------------
    # End time
    # -----------------------------------------------------

    if not validate_time(
        data["end_time"],
        "end_time"
    ):
        return False, "end_time must be in HH:MM format"

    # -----------------------------------------------------
    # Compare start and end time
    # -----------------------------------------------------

    start_hour, start_minute = map(
        int,
        data["start_time"].split(":")
    )

    end_hour, end_minute = map(
        int,
        data["end_time"].split(":")
    )

    start_minutes = (
        start_hour * 60
        + start_minute
    )

    end_minutes = (
        end_hour * 60
        + end_minute
    )

    if end_minutes <= start_minutes:

        return (
            False,
            "end_time must be later than start_time"
        )

    # -----------------------------------------------------
    # Slot duration validation
    # -----------------------------------------------------

    if "slot_duration" in data:

        try:
            slot_duration = int(
                data["slot_duration"]
            )

            if slot_duration <= 0:
                return (
                    False,
                    "slot_duration must be greater than 0"
                )

        except (ValueError, TypeError):

            return (
                False,
                "slot_duration must be a valid number"
            )

    # -----------------------------------------------------
    # Break time validation
    # -----------------------------------------------------

    if data.get("break_start") is not None:

        if not validate_time(
            data["break_start"],
            "break_start"
        ):
            return (
                False,
                "break_start must be in HH:MM format"
            )

    if data.get("break_end") is not None:

        if not validate_time(
            data["break_end"],
            "break_end"
        ):
            return (
                False,
                "break_end must be in HH:MM format"
            )

    # -----------------------------------------------------
    # Break start/end consistency
    # -----------------------------------------------------

    if (
        data.get("break_start") is not None
        and data.get("break_end") is not None
    ):

        break_start_hour, break_start_minute = map(
            int,
            data["break_start"].split(":")
        )

        break_end_hour, break_end_minute = map(
            int,
            data["break_end"].split(":")
        )

        break_start_minutes = (
            break_start_hour * 60
            + break_start_minute
        )

        break_end_minutes = (
            break_end_hour * 60
            + break_end_minute
        )

        if break_end_minutes <= break_start_minutes:

            return (
                False,
                "break_end must be later than break_start"
            )

        # Break must be inside working hours

        if (
            break_start_minutes < start_minutes
            or break_end_minutes > end_minutes
        ):

            return (
                False,
                "Break time must be within working hours"
            )

    # -----------------------------------------------------
    # Availability validation
    # -----------------------------------------------------

    if "is_available" in data:

        if data["is_available"] is not None:

            if not isinstance(
                data["is_available"],
                bool
            ):

                return (
                    False,
                    "is_available must be true or false"
                )

    # -----------------------------------------------------
    # Validation successful
    # -----------------------------------------------------

    return True, None