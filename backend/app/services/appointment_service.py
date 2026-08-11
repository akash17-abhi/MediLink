from datetime import datetime

from app.models.appointment import Appointment
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.hospital import Hospital

from app.repositories.appointment_repository import (
    AppointmentRepository
)

from app.services.email_service import EmailService


class AppointmentService:

    # =========================================================
    # CREATE APPOINTMENT
    # =========================================================

    @staticmethod
    def create(data):

        # -----------------------------------------------------
        # Check patient
        # -----------------------------------------------------

        patient = Patient.query.get(
            data["patient_id"]
        )

        if not patient:
            return None, "Patient not found"

        # -----------------------------------------------------
        # Check doctor
        # -----------------------------------------------------

        doctor = Doctor.query.get(
            data["doctor_id"]
        )

        if not doctor:
            return None, "Doctor not found"

        # -----------------------------------------------------
        # Check hospital
        # -----------------------------------------------------

        hospital = Hospital.query.get(
            data["hospital_id"]
        )

        if not hospital:
            return None, "Hospital not found"

        # -----------------------------------------------------
        # Convert appointment date
        # -----------------------------------------------------

        try:

            appointment_date = datetime.strptime(
                data["appointment_date"],
                "%Y-%m-%d"
            ).date()

        except (ValueError, TypeError):

            return (
                None,
                "appointment_date must be in YYYY-MM-DD format"
            )

        # -----------------------------------------------------
        # Convert appointment time
        # Accept both HH:MM and HH:MM:SS
        # -----------------------------------------------------

        appointment_time = None

        for time_format in (
            "%H:%M",
            "%H:%M:%S"
        ):

            try:

                appointment_time = datetime.strptime(
                    data["appointment_time"],
                    time_format
                ).time()

                break

            except (ValueError, TypeError):
                continue

        if appointment_time is None:

            return (
                None,
                "appointment_time must be in HH:MM or HH:MM:SS format"
            )

        # -----------------------------------------------------
        # Create appointment
        # -----------------------------------------------------

        appointment = Appointment(
            patient_id=data["patient_id"],
            doctor_id=data["doctor_id"],
            hospital_id=data["hospital_id"],

            appointment_date=appointment_date,
            appointment_time=appointment_time,

            reason=data.get("reason"),

            status=data.get(
                "status",
                "Pending"
            ),

            consultation_mode=data.get(
                "consultation_mode",
                "Offline"
            ),

            payment_status=data.get(
                "payment_status",
                "Pending"
            ),

            notes=data.get("notes")
        )

        # -----------------------------------------------------
        # Save appointment
        # -----------------------------------------------------

        AppointmentRepository.create(
            appointment
        )

        # -----------------------------------------------------
        # Send confirmation email
        # if appointment is created as Confirmed
        # -----------------------------------------------------

        if (
            appointment.status
            and appointment.status.lower() == "confirmed"
        ):

            EmailService.send_appointment_confirmation(

                patient_email=patient.email,

                patient_name=patient.full_name,

                doctor_name=doctor.full_name,

                appointment_date=(
                    appointment.appointment_date.strftime(
                        "%d %B %Y"
                    )
                ),

                appointment_time=(
                    appointment.appointment_time.strftime(
                        "%I:%M %p"
                    )
                ),

                hospital_name=hospital.name
            )

        return appointment, None

    # =========================================================
    # GET ALL APPOINTMENTS
    # =========================================================

    @staticmethod
    def get_all():

        return AppointmentRepository.get_all()

    # =========================================================
    # GET APPOINTMENT BY ID
    # =========================================================

    @staticmethod
    def get_by_id(appointment_id):

        return AppointmentRepository.get_by_id(
            appointment_id
        )

    # =========================================================
    # UPDATE APPOINTMENT
    # =========================================================

    @staticmethod
    def update(
        appointment_id,
        data
    ):

        appointment = AppointmentRepository.get_by_id(
            appointment_id
        )

        if not appointment:
            return None, "Appointment not found"

        # -----------------------------------------------------
        # Previous status
        # -----------------------------------------------------

        previous_status = appointment.status

        # -----------------------------------------------------
        # Validate patient if changed
        # -----------------------------------------------------

        if "patient_id" in data:

            patient = Patient.query.get(
                data["patient_id"]
            )

            if not patient:
                return None, "Patient not found"

        else:

            patient = appointment.patient

        # -----------------------------------------------------
        # Validate doctor if changed
        # -----------------------------------------------------

        if "doctor_id" in data:

            doctor = Doctor.query.get(
                data["doctor_id"]
            )

            if not doctor:
                return None, "Doctor not found"

        else:

            doctor = appointment.doctor

        # -----------------------------------------------------
        # Validate hospital if changed
        # -----------------------------------------------------

        if "hospital_id" in data:

            hospital = Hospital.query.get(
                data["hospital_id"]
            )

            if not hospital:
                return None, "Hospital not found"

        else:

            hospital = appointment.hospital

        # -----------------------------------------------------
        # Convert appointment date
        # -----------------------------------------------------

        if "appointment_date" in data:

            try:

                data["appointment_date"] = datetime.strptime(
                    data["appointment_date"],
                    "%Y-%m-%d"
                ).date()

            except (ValueError, TypeError):

                return (
                    None,
                    "appointment_date must be in YYYY-MM-DD format"
                )

        # -----------------------------------------------------
        # Convert appointment time
        # -----------------------------------------------------

        if "appointment_time" in data:

            converted_time = None

            for time_format in (
                "%H:%M",
                "%H:%M:%S"
            ):

                try:

                    converted_time = datetime.strptime(
                        data["appointment_time"],
                        time_format
                    ).time()

                    break

                except (ValueError, TypeError):
                    continue

            if converted_time is None:

                return (
                    None,
                    "appointment_time must be in HH:MM or HH:MM:SS format"
                )

            data["appointment_time"] = converted_time

        # -----------------------------------------------------
        # Fields allowed to update
        # -----------------------------------------------------

        allowed_fields = [
            "patient_id",
            "doctor_id",
            "hospital_id",
            "appointment_date",
            "appointment_time",
            "reason",
            "status",
            "consultation_mode",
            "payment_status",
            "notes"
        ]

        for key, value in data.items():

            if key in allowed_fields:

                setattr(
                    appointment,
                    key,
                    value
                )

        # -----------------------------------------------------
        # Save changes
        # -----------------------------------------------------

        AppointmentRepository.update()

        # -----------------------------------------------------
        # Refresh relationships after update
        # -----------------------------------------------------

        patient = appointment.patient
        doctor = appointment.doctor
        hospital = appointment.hospital

        # =====================================================
        # CONFIRMATION EMAIL
        # =====================================================

        if (
            appointment.status
            and appointment.status.lower() == "confirmed"
            and (
                not previous_status
                or previous_status.lower() != "confirmed"
            )
        ):

            EmailService.send_appointment_confirmation(

                patient_email=patient.email,

                patient_name=patient.full_name,

                doctor_name=doctor.full_name,

                appointment_date=(
                    appointment.appointment_date.strftime(
                        "%d %B %Y"
                    )
                ),

                appointment_time=(
                    appointment.appointment_time.strftime(
                        "%I:%M %p"
                    )
                ),

                hospital_name=hospital.name
            )

        # =====================================================
        # CANCELLATION EMAIL
        # =====================================================

        if (
            appointment.status
            and appointment.status.lower() == "cancelled"
            and (
                not previous_status
                or previous_status.lower() != "cancelled"
            )
        ):

            EmailService.send_appointment_cancellation(

                patient_email=patient.email,

                patient_name=patient.full_name,

                doctor_name=doctor.full_name,

                appointment_date=(
                    appointment.appointment_date.strftime(
                        "%d %B %Y"
                    )
                ),

                appointment_time=(
                    appointment.appointment_time.strftime(
                        "%I:%M %p"
                    )
                ),

                reason=data.get(
                    "cancellation_reason"
                )
            )

        return appointment, None

    # =========================================================
    # DELETE APPOINTMENT
    # =========================================================

    @staticmethod
    def delete(appointment_id):

        appointment = AppointmentRepository.get_by_id(
            appointment_id
        )

        if not appointment:
            return False

        AppointmentRepository.delete(
            appointment
        )

        return True