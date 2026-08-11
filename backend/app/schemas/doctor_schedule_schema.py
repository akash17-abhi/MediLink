# =========================================================
# DOCTOR SCHEDULE SCHEMA
# =========================================================


def schedule_to_dict(schedule):

    return {
        # -------------------------------------------------
        # Basic information
        # -------------------------------------------------

        "id": schedule.id,

        "doctor_id": schedule.doctor_id,

        "day_of_week": schedule.day_of_week,

        # -------------------------------------------------
        # Working time
        # -------------------------------------------------

        "start_time": (
            schedule.start_time.strftime("%H:%M")
            if schedule.start_time
            else None
        ),

        "end_time": (
            schedule.end_time.strftime("%H:%M")
            if schedule.end_time
            else None
        ),

        # -------------------------------------------------
        # Appointment slot
        # -------------------------------------------------

        "slot_duration": schedule.slot_duration,

        # -------------------------------------------------
        # Break time
        # -------------------------------------------------

        "break_start": (
            schedule.break_start.strftime("%H:%M")
            if schedule.break_start
            else None
        ),

        "break_end": (
            schedule.break_end.strftime("%H:%M")
            if schedule.break_end
            else None
        ),

        # -------------------------------------------------
        # Status
        # -------------------------------------------------

        "is_available": schedule.is_available,

        # -------------------------------------------------
        # Timestamps
        # -------------------------------------------------

        "created_at": (
            schedule.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if schedule.created_at
            else None
        ),

        "updated_at": (
            schedule.updated_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if schedule.updated_at
            else None
        )
    }