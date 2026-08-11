from datetime import datetime

from app.models.doctor import Doctor
from app.models.doctor_schedule import DoctorSchedule
from app.repositories.doctor_schedule_repository import (
    DoctorScheduleRepository
)


class DoctorScheduleService:

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
            return None, "Doctor not found"

        # -----------------------------------------------------
        # Create schedule
        # -----------------------------------------------------

        schedule = DoctorSchedule(
            doctor_id=data["doctor_id"],

            day_of_week=data["day_of_week"],

            start_time=datetime.strptime(
                data["start_time"],
                "%H:%M"
            ).time(),

            end_time=datetime.strptime(
                data["end_time"],
                "%H:%M"
            ).time(),

            slot_duration=data.get(
                "slot_duration",
                30
            ),

            break_start=(
                datetime.strptime(
                    data["break_start"],
                    "%H:%M"
                ).time()
                if data.get("break_start")
                else None
            ),

            break_end=(
                datetime.strptime(
                    data["break_end"],
                    "%H:%M"
                ).time()
                if data.get("break_end")
                else None
            ),

            is_available=data.get(
                "is_available",
                True
            )
        )

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
        # Find schedule
        # -----------------------------------------------------

        schedule = DoctorScheduleRepository.get_by_id(
            schedule_id
        )

        if not schedule:
            return None

        # -----------------------------------------------------
        # Convert time fields before repository update
        # -----------------------------------------------------

        update_data = {}

        # -----------------------------------------------------
        # Day
        # -----------------------------------------------------

        if "day_of_week" in data:

            update_data["day_of_week"] = (
                data["day_of_week"]
            )

        # -----------------------------------------------------
        # Start time
        # -----------------------------------------------------

        if "start_time" in data:

            update_data["start_time"] = (
                datetime.strptime(
                    data["start_time"],
                    "%H:%M"
                ).time()
            )

        # -----------------------------------------------------
        # End time
        # -----------------------------------------------------

        if "end_time" in data:

            update_data["end_time"] = (
                datetime.strptime(
                    data["end_time"],
                    "%H:%M"
                ).time()
            )

        # -----------------------------------------------------
        # Slot duration
        # -----------------------------------------------------

        if "slot_duration" in data:

            update_data["slot_duration"] = (
                data["slot_duration"]
            )

        # -----------------------------------------------------
        # Break start
        # -----------------------------------------------------

        if "break_start" in data:

            update_data["break_start"] = (
                datetime.strptime(
                    data["break_start"],
                    "%H:%M"
                ).time()
                if data["break_start"]
                else None
            )

        # -----------------------------------------------------
        # Break end
        # -----------------------------------------------------

        if "break_end" in data:

            update_data["break_end"] = (
                datetime.strptime(
                    data["break_end"],
                    "%H:%M"
                ).time()
                if data["break_end"]
                else None
            )

        # -----------------------------------------------------
        # Availability
        # -----------------------------------------------------

        if "is_available" in data:

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

        return updated_schedule

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