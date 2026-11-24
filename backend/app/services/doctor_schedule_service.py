from datetime import datetime

from app.models.doctor import Doctor
from app.models.doctor_schedule import DoctorSchedule
from app.repositories.doctor_schedule_repository import (
    DoctorScheduleRepository
)


class DoctorScheduleService:

    # =========================================================
    # HELPER: CONVERT HH:MM STRING TO TIME
    # =========================================================

    @staticmethod
    def _parse_time(value):

        if value is None:
            return None

        if hasattr(value, "hour"):
            return value

        return datetime.strptime(
            value,
            "%H:%M"
        ).time()

    # =========================================================
    # HELPER: CHECK SCHEDULE OVERLAP
    # =========================================================

    @staticmethod
    def _has_overlap(
        doctor_id,
        day_of_week,
        start_time,
        end_time,
        exclude_schedule_id=None
    ):
        """
        Check whether the proposed schedule overlaps
        with an existing schedule for the same doctor
        and same day.

        Example:

        Existing:
            09:00 - 13:00

        New:
            11:00 - 15:00

        Result:
            Overlap = True
        """

        schedules = DoctorScheduleRepository.get_by_doctor(
            doctor_id
        )

        for existing in schedules:

            # -------------------------------------------------
            # Ignore the schedule currently being updated
            # -------------------------------------------------

            if (
                exclude_schedule_id is not None
                and existing.id == exclude_schedule_id
            ):
                continue

            # -------------------------------------------------
            # Only compare schedules on the same day
            # -------------------------------------------------

            if (
                existing.day_of_week.strip().lower()
                != day_of_week.strip().lower()
            ):
                continue

            # -------------------------------------------------
            # Ignore unavailable schedules
            # -------------------------------------------------

            if not existing.is_available:
                continue

            # -------------------------------------------------
            # Overlap condition:
            #
            # new_start < existing_end
            # AND
            # new_end > existing_start
            # -------------------------------------------------

            if (
                start_time < existing.end_time
                and end_time > existing.start_time
            ):
                return True

        return False

    # =========================================================
    # CREATE SCHEDULE
    # =========================================================

    @staticmethod
    def create(data):

        # -----------------------------------------------------
        # Check doctor
        # -----------------------------------------------------

        doctor = Doctor.query.get(
            data["doctor_id"]
        )

        if not doctor:

            return (
                None,
                "Doctor not found"
            )

        # -----------------------------------------------------
        # Convert time fields
        # -----------------------------------------------------

        start_time = DoctorScheduleService._parse_time(
            data["start_time"]
        )

        end_time = DoctorScheduleService._parse_time(
            data["end_time"]
        )

        break_start = DoctorScheduleService._parse_time(
            data.get("break_start")
        )

        break_end = DoctorScheduleService._parse_time(
            data.get("break_end")
        )

        # -----------------------------------------------------
        # Check overlapping schedule
        # -----------------------------------------------------

        if DoctorScheduleService._has_overlap(
            doctor_id=data["doctor_id"],
            day_of_week=data["day_of_week"],
            start_time=start_time,
            end_time=end_time
        ):

            return (
                None,
                (
                    "Doctor already has an overlapping "
                    "schedule for this day"
                )
            )

        # -----------------------------------------------------
        # Create schedule
        # -----------------------------------------------------

        schedule = DoctorSchedule(

            doctor_id=data["doctor_id"],

            day_of_week=data["day_of_week"],

            start_time=start_time,

            end_time=end_time,

            slot_duration=data.get(
                "slot_duration",
                30
            ),

            break_start=break_start,

            break_end=break_end,

            is_available=data.get(
                "is_available",
                True
            )
        )

        # -----------------------------------------------------
        # Save
        # -----------------------------------------------------

        DoctorScheduleRepository.create(
            schedule
        )

        return schedule, None

    # =========================================================
    # GET ALL SCHEDULES
    # =========================================================

    @staticmethod
    def get_all():

        return DoctorScheduleRepository.get_all()

    # =========================================================
    # GET SCHEDULE BY ID
    # =========================================================

    @staticmethod
    def get_by_id(schedule_id):

        return DoctorScheduleRepository.get_by_id(
            schedule_id
        )

    # =========================================================
    # GET SCHEDULES BY DOCTOR
    # =========================================================

    @staticmethod
    def get_by_doctor(doctor_id):

        return DoctorScheduleRepository.get_by_doctor(
            doctor_id
        )

    # =========================================================
    # UPDATE SCHEDULE
    # =========================================================

    @staticmethod
    def update(schedule_id, data):

        # -----------------------------------------------------
        # Find existing schedule
        # -----------------------------------------------------

        schedule = DoctorScheduleRepository.get_by_id(
            schedule_id
        )

        if not schedule:

            return None, "Schedule not found"

        # -----------------------------------------------------
        # Determine resulting values
        #
        # We use existing values when a field is not supplied.
        # -----------------------------------------------------

        doctor_id = schedule.doctor_id

        day_of_week = schedule.day_of_week

        start_time = schedule.start_time

        end_time = schedule.end_time

        # -----------------------------------------------------
        # Doctor
        #
        # Allow changing doctor_id if supplied.
        # -----------------------------------------------------

        if "doctor_id" in data:

            try:

                doctor_id = int(
                    data["doctor_id"]
                )

            except (ValueError, TypeError):

                return (
                    None,
                    "doctor_id must be a valid number"
                )

            if doctor_id <= 0:

                return (
                    None,
                    "doctor_id must be a valid positive number"
                )

            doctor = Doctor.query.get(
                doctor_id
            )

            if not doctor:

                return (
                    None,
                    "Doctor not found"
                )

        # -----------------------------------------------------
        # Day
        # -----------------------------------------------------

        if "day_of_week" in data:

            day_of_week = str(
                data["day_of_week"]
            ).strip().capitalize()

        # -----------------------------------------------------
        # Start time
        # -----------------------------------------------------

        if "start_time" in data:

            try:

                start_time = DoctorScheduleService._parse_time(
                    data["start_time"]
                )

            except (ValueError, TypeError):

                return (
                    None,
                    "start_time must be in HH:MM format"
                )

        # -----------------------------------------------------
        # End time
        # -----------------------------------------------------

        if "end_time" in data:

            try:

                end_time = DoctorScheduleService._parse_time(
                    data["end_time"]
                )

            except (ValueError, TypeError):

                return (
                    None,
                    "end_time must be in HH:MM format"
                )

        # -----------------------------------------------------
        # Validate resulting time range
        # -----------------------------------------------------

        if end_time <= start_time:

            return (
                None,
                "end_time must be later than start_time"
            )

        # -----------------------------------------------------
        # Check overlapping schedule
        # -----------------------------------------------------

        if DoctorScheduleService._has_overlap(
            doctor_id=doctor_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            exclude_schedule_id=schedule.id
        ):

            return (
                None,
                (
                    "Doctor already has an overlapping "
                    "schedule for this day"
                )
            )

        # -----------------------------------------------------
        # Prepare update data
        # -----------------------------------------------------

        update_data = {}

        # -----------------------------------------------------
        # Doctor
        # -----------------------------------------------------

        if "doctor_id" in data:

            update_data["doctor_id"] = doctor_id

        # -----------------------------------------------------
        # Day
        # -----------------------------------------------------

        if "day_of_week" in data:

            update_data["day_of_week"] = day_of_week

        # -----------------------------------------------------
        # Start time
        # -----------------------------------------------------

        if "start_time" in data:

            update_data["start_time"] = start_time

        # -----------------------------------------------------
        # End time
        # -----------------------------------------------------

        if "end_time" in data:

            update_data["end_time"] = end_time

        # -----------------------------------------------------
        # Slot duration
        # -----------------------------------------------------

        if "slot_duration" in data:

            try:

                slot_duration = int(
                    data["slot_duration"]
                )

            except (ValueError, TypeError):

                return (
                    None,
                    "slot_duration must be a valid number"
                )

            if slot_duration <= 0:

                return (
                    None,
                    "slot_duration must be greater than 0"
                )

            update_data["slot_duration"] = slot_duration

        # -----------------------------------------------------
        # Break start
        # -----------------------------------------------------

        if "break_start" in data:

            if data["break_start"]:

                try:

                    update_data["break_start"] = (
                        DoctorScheduleService._parse_time(
                            data["break_start"]
                        )
                    )

                except (ValueError, TypeError):

                    return (
                        None,
                        "break_start must be in HH:MM format"
                    )

            else:

                update_data["break_start"] = None

        # -----------------------------------------------------
        # Break end
        # -----------------------------------------------------

        if "break_end" in data:

            if data["break_end"]:

                try:

                    update_data["break_end"] = (
                        DoctorScheduleService._parse_time(
                            data["break_end"]
                        )
                    )

                except (ValueError, TypeError):

                    return (
                        None,
                        "break_end must be in HH:MM format"
                    )

            else:

                update_data["break_end"] = None

        # -----------------------------------------------------
        # Availability
        # -----------------------------------------------------

        if "is_available" in data:

            if not isinstance(
                data["is_available"],
                bool
            ):

                return (
                    None,
                    "is_available must be true or false"
                )

            update_data["is_available"] = (
                data["is_available"]
            )

        # -----------------------------------------------------
        # Update database
        # -----------------------------------------------------

        updated_schedule = (
            DoctorScheduleRepository.update(
                schedule,
                update_data
            )
        )

        return updated_schedule, None

    # =========================================================
    # DELETE SCHEDULE
    # =========================================================

    @staticmethod
    def delete(schedule_id):

        schedule = DoctorScheduleRepository.get_by_id(
            schedule_id
        )

        if not schedule:

            return False

        DoctorScheduleRepository.delete(
            schedule
        )

        return True