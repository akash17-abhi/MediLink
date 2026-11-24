from datetime import datetime, date

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
        # Check doctor active
        # -----------------------------------------------------

        if not doctor.is_active:
            return None, "Doctor is currently inactive"

        # -----------------------------------------------------
        # Check hospital
        # -----------------------------------------------------

        hospital = Hospital.query.get(
            data["hospital_id"]
        )

        if not hospital:
            return None, "Hospital not found"

        # -----------------------------------------------------
        # Check hospital active
        # -----------------------------------------------------

        if not hospital.is_active:
            return None, "Hospital is currently inactive"

        # -----------------------------------------------------
        # Check doctor belongs to hospital
        # -----------------------------------------------------

        if doctor.hospital_id != hospital.id:

            return (
                None,
                "Doctor does not belong to the selected hospital"
            )

        # -----------------------------------------------------
        # Convert appointment date
        # -----------------------------------------------------

        try:

            appointment_date = datetime.strptime(
                str(data["appointment_date"]).strip(),
                "%Y-%m-%d"
            ).date()

        except (ValueError, TypeError):

            return (
                None,
                "appointment_date must be in YYYY-MM-DD format"
            )

        # -----------------------------------------------------
        # Prevent appointments in the past
        # -----------------------------------------------------

        if appointment_date < date.today():

            return (
                None,
                "Appointment date cannot be in the past"
            )

        # -----------------------------------------------------
        # Convert appointment time
        # -----------------------------------------------------

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

            except (ValueError, TypeError):

                continue

        if appointment_time is None:

            return (
                None,
                "appointment_time must be in HH:MM or HH:MM:SS format"
            )

        # -----------------------------------------------------
        # Validate status
        # -----------------------------------------------------

        status = data.get(
            "status",
            "Pending"
        )

        valid_statuses = {
            "Pending",
            "Confirmed",
            "Cancelled",
            "Completed",
            "No Show"
        }

        if status not in valid_statuses:

            return (
                None,
                "Invalid appointment status"
            )

        # -----------------------------------------------------
        # Validate consultation mode
        # -----------------------------------------------------

        consultation_mode = data.get(
            "consultation_mode",
            "Offline"
        )

        valid_consultation_modes = {
            "Offline",
            "Online"
        }

        if consultation_mode not in valid_consultation_modes:

            return (
                None,
                "Invalid consultation mode"
            )

        # -----------------------------------------------------
        # Validate payment status
        # -----------------------------------------------------

        payment_status = data.get(
            "payment_status",
            "Pending"
        )

        valid_payment_statuses = {
            "Pending",
            "Paid",
            "Failed",
            "Refunded"
        }

        if payment_status not in valid_payment_statuses:

            return (
                None,
                "Invalid payment status"
            )

        # -----------------------------------------------------
        # Check appointment conflict
        # -----------------------------------------------------

        existing_appointments = Appointment.query.filter_by(
            doctor_id=doctor.id,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).all()

        for existing in existing_appointments:

            if existing.status not in {
                "Cancelled",
                "Completed"
            }:

                return (
                    None,
                    "Doctor already has an appointment at this date and time"
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

            status=status,

            consultation_mode=consultation_mode,

            payment_status=payment_status,

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

        # -----------------------------------------------------
        # Find appointment
        # -----------------------------------------------------

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
        # Work on a copy
        # -----------------------------------------------------

        update_data = dict(data)

        # -----------------------------------------------------
        # Remove non-database field
        # -----------------------------------------------------

        cancellation_reason = update_data.pop(
            "cancellation_reason",
            None
        )

        # -----------------------------------------------------
        # Current patient
        # -----------------------------------------------------

        if "patient_id" in update_data:

            patient = Patient.query.get(
                update_data["patient_id"]
            )

            if not patient:

                return None, "Patient not found"

        else:

            patient = appointment.patient

        # -----------------------------------------------------
        # Current doctor
        # -----------------------------------------------------

        if "doctor_id" in update_data:

            doctor = Doctor.query.get(
                update_data["doctor_id"]
            )

            if not doctor:

                return None, "Doctor not found"

            if not doctor.is_active:

                return None, "Doctor is currently inactive"

        else:

            doctor = appointment.doctor

        # -----------------------------------------------------
        # Current hospital
        # -----------------------------------------------------

        if "hospital_id" in update_data:

            hospital = Hospital.query.get(
                update_data["hospital_id"]
            )

            if not hospital:

                return None, "Hospital not found"

        else:

            hospital = appointment.hospital

        # -----------------------------------------------------
        # Check hospital active
        # -----------------------------------------------------

        if not hospital.is_active:

            return None, "Hospital is currently inactive"

        # -----------------------------------------------------
        # Check doctor belongs to hospital
        # -----------------------------------------------------

        if doctor.hospital_id != hospital.id:

            return (
                None,
                "Doctor does not belong to the selected hospital"
            )

        # -----------------------------------------------------
        # Convert appointment date
        # -----------------------------------------------------

        if "appointment_date" in update_data:

            try:

                converted_date = datetime.strptime(
                    str(
                        update_data["appointment_date"]
                    ).strip(),
                    "%Y-%m-%d"
                ).date()

            except (ValueError, TypeError):

                return (
                    None,
                    "appointment_date must be in YYYY-MM-DD format"
                )

            # Prevent past appointment dates

            if converted_date < date.today():

                return (
                    None,
                    "Appointment date cannot be in the past"
                )

            update_data["appointment_date"] = converted_date

        # -----------------------------------------------------
        # Convert appointment time
        # -----------------------------------------------------

        if "appointment_time" in update_data:

            converted_time = None

            time_value = str(
                update_data["appointment_time"]
            ).strip()

            for time_format in (
                "%H:%M",
                "%H:%M:%S"
            ):

                try:

                    converted_time = datetime.strptime(
                        time_value,
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

            update_data["appointment_time"] = converted_time

        # -----------------------------------------------------
        # Validate status
        # -----------------------------------------------------

        if "status" in update_data:

            valid_statuses = {
                "Pending",
                "Confirmed",
                "Cancelled",
                "Completed",
                "No Show"
            }

            if update_data["status"] not in valid_statuses:

                return (
                    None,
                    "Invalid appointment status"
                )

        # -----------------------------------------------------
        # Validate consultation mode
        # -----------------------------------------------------

        if "consultation_mode" in update_data:

            valid_modes = {
                "Offline",
                "Online"
            }

            if update_data["consultation_mode"] not in valid_modes:

                return (
                    None,
                    "Invalid consultation mode"
                )

        # -----------------------------------------------------
        # Validate payment status
        # -----------------------------------------------------

        if "payment_status" in update_data:

            valid_payment_statuses = {
                "Pending",
                "Paid",
                "Failed",
                "Refunded"
            }

            if (
                update_data["payment_status"]
                not in valid_payment_statuses
            ):

                return (
                    None,
                    "Invalid payment status"
                )

        # -----------------------------------------------------
        # Determine final appointment date/time
        # -----------------------------------------------------

        final_date = update_data.get(
            "appointment_date",
            appointment.appointment_date
        )

        final_time = update_data.get(
            "appointment_time",
            appointment.appointment_time
        )

        final_doctor_id = update_data.get(
            "doctor_id",
            appointment.doctor_id
        )

        # -----------------------------------------------------
        # Check appointment conflict
        # -----------------------------------------------------

        existing_appointments = Appointment.query.filter_by(
            doctor_id=final_doctor_id,
            appointment_date=final_date,
            appointment_time=final_time
        ).all()

        for existing in existing_appointments:

            if existing.id == appointment.id:
                continue

            if existing.status not in {
                "Cancelled",
                "Completed"
            }:

                return (
                    None,
                    "Doctor already has an appointment at this date and time"
                )

        # -----------------------------------------------------
        # Allowed fields
        # -----------------------------------------------------

        allowed_fields = {
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
        }

        # -----------------------------------------------------
        # Filter update data
        # -----------------------------------------------------

        filtered_update_data = {
            key: value
            for key, value in update_data.items()
            if key in allowed_fields
        }

        # -----------------------------------------------------
        # Update database
        # -----------------------------------------------------

        updated_appointment = (
            AppointmentRepository.update(
                appointment,
                filtered_update_data
            )
        )

        # -----------------------------------------------------
        # Refresh relationships
        # -----------------------------------------------------

        patient = updated_appointment.patient
        doctor = updated_appointment.doctor
        hospital = updated_appointment.hospital

        # =====================================================
        # CONFIRMATION EMAIL
        # =====================================================

        if (
            updated_appointment.status
            and updated_appointment.status.lower() == "confirmed"
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
                    updated_appointment.appointment_date.strftime(
                        "%d %B %Y"
                    )
                ),

                appointment_time=(
                    updated_appointment.appointment_time.strftime(
                        "%I:%M %p"
                    )
                ),

                hospital_name=hospital.name
            )

        # =====================================================
        # CANCELLATION EMAIL
        # =====================================================

        if (
            updated_appointment.status
            and updated_appointment.status.lower() == "cancelled"
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
                    updated_appointment.appointment_date.strftime(
                        "%d %B %Y"
                    )
                ),

                appointment_time=(
                    updated_appointment.appointment_time.strftime(
                        "%I:%M %p"
                    )
                ),

                reason=cancellation_reason
            )

        return updated_appointment, None

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