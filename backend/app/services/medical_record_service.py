from datetime import datetime, date

from app.models.medical_record import MedicalRecord

from app.repositories.medical_record_repository import (
    MedicalRecordRepository
)

from app.repositories.patient_repository import (
    PatientRepository
)

from app.repositories.doctor_repository import (
    DoctorRepository
)

from app.repositories.appointment_repository import (
    AppointmentRepository
)


class MedicalRecordService:

    # =========================================================
    # CREATE MEDICAL RECORD
    # =========================================================

    @staticmethod
    def create(data):

        # -----------------------------------------------------
        # Check patient
        # -----------------------------------------------------

        patient = PatientRepository.get_by_id(
            data["patient_id"]
        )

        if not patient:

            return (
                None,
                "Patient not found"
            )

        # -----------------------------------------------------
        # Check doctor
        # -----------------------------------------------------

        doctor = DoctorRepository.get_by_id(
            data["doctor_id"]
        )

        if not doctor:

            return (
                None,
                "Doctor not found"
            )

        # -----------------------------------------------------
        # Check appointment if provided
        # -----------------------------------------------------

        appointment = None

        if data.get("appointment_id") is not None:

            appointment = AppointmentRepository.get_by_id(
                data["appointment_id"]
            )

            if not appointment:

                return (
                    None,
                    "Appointment not found"
                )

            # -------------------------------------------------
            # Make sure appointment belongs to patient
            # -------------------------------------------------

            if appointment.patient_id != data["patient_id"]:

                return (
                    None,
                    "Appointment does not belong to this patient"
                )

            # -------------------------------------------------
            # Make sure appointment belongs to doctor
            # -------------------------------------------------

            if appointment.doctor_id != data["doctor_id"]:

                return (
                    None,
                    "Appointment does not belong to this doctor"
                )

        # =====================================================
        # FOLLOW-UP DATE
        # =====================================================

        follow_up = None

        if data.get("follow_up_date"):

            try:

                follow_up = datetime.strptime(
                    data["follow_up_date"],
                    "%Y-%m-%d"
                ).date()

            except (ValueError, TypeError):

                return (
                    None,
                    "follow_up_date must be in YYYY-MM-DD format"
                )

            # -------------------------------------------------
            # Follow-up cannot be in the past
            # -------------------------------------------------

            if follow_up < date.today():

                return (
                    None,
                    "follow_up_date cannot be in the past"
                )

        # =====================================================
        # CREATE RECORD
        # =====================================================

        record = MedicalRecord(

            patient_id=data["patient_id"],

            doctor_id=data["doctor_id"],

            appointment_id=data.get(
                "appointment_id"
            ),

            diagnosis=data["diagnosis"],

            symptoms=data.get(
                "symptoms"
            ),

            prescription=data.get(
                "prescription"
            ),

            lab_tests=data.get(
                "lab_tests"
            ),

            notes=data.get(
                "notes"
            ),

            follow_up_date=follow_up
        )

        # =====================================================
        # SAVE
        # =====================================================

        MedicalRecordRepository.create(
            record
        )

        return record, None

    # =========================================================
    # GET ALL
    # =========================================================

    @staticmethod
    def get_all():

        return MedicalRecordRepository.get_all()

    # =========================================================
    # GET BY ID
    # =========================================================

    @staticmethod
    def get_by_id(record_id):

        return MedicalRecordRepository.get_by_id(
            record_id
        )

    # =========================================================
    # UPDATE
    # =========================================================

    @staticmethod
    def update(record_id, data):

        record = MedicalRecordRepository.get_by_id(
            record_id
        )

        if not record:

            return (
                None,
                "Medical record not found"
            )

        # -----------------------------------------------------
        # Validate patient if being changed
        # -----------------------------------------------------

        if "patient_id" in data:

            patient = PatientRepository.get_by_id(
                data["patient_id"]
            )

            if not patient:

                return (
                    None,
                    "Patient not found"
                )

        # -----------------------------------------------------
        # Validate doctor if being changed
        # -----------------------------------------------------

        if "doctor_id" in data:

            doctor = DoctorRepository.get_by_id(
                data["doctor_id"]
            )

            if not doctor:

                return (
                    None,
                    "Doctor not found"
                )

        # -----------------------------------------------------
        # Validate appointment if being changed
        # -----------------------------------------------------

        if "appointment_id" in data:

            if data["appointment_id"] is None:

                pass

            else:

                appointment = (
                    AppointmentRepository.get_by_id(
                        data["appointment_id"]
                    )
                )

                if not appointment:

                    return (
                        None,
                        "Appointment not found"
                    )

                new_patient_id = data.get(
                    "patient_id",
                    record.patient_id
                )

                new_doctor_id = data.get(
                    "doctor_id",
                    record.doctor_id
                )

                if (
                    appointment.patient_id
                    != new_patient_id
                ):

                    return (
                        None,
                        "Appointment does not belong to this patient"
                    )

                if (
                    appointment.doctor_id
                    != new_doctor_id
                ):

                    return (
                        None,
                        "Appointment does not belong to this doctor"
                    )

        # =====================================================
        # FOLLOW-UP DATE
        # =====================================================

        if "follow_up_date" in data:

            if data["follow_up_date"]:

                try:

                    data["follow_up_date"] = (
                        datetime.strptime(
                            data["follow_up_date"],
                            "%Y-%m-%d"
                        ).date()
                    )

                except (ValueError, TypeError):

                    return (
                        None,
                        "follow_up_date must be in YYYY-MM-DD format"
                    )

                if (
                    data["follow_up_date"]
                    < date.today()
                ):

                    return (
                        None,
                        "follow_up_date cannot be in the past"
                    )

            else:

                data["follow_up_date"] = None

        # =====================================================
        # UPDATE ALLOWED FIELDS
        # =====================================================

        allowed_fields = [
            "patient_id",
            "doctor_id",
            "appointment_id",
            "diagnosis",
            "symptoms",
            "prescription",
            "lab_tests",
            "notes",
            "follow_up_date"
        ]

        for key, value in data.items():

            if key in allowed_fields:

                setattr(
                    record,
                    key,
                    value
                )

        # =====================================================
        # SAVE
        # =====================================================

        MedicalRecordRepository.update()

        return record, None

    # =========================================================
    # DELETE
    # =========================================================

    @staticmethod
    def delete(record_id):

        record = MedicalRecordRepository.get_by_id(
            record_id
        )

        if not record:

            return False

        MedicalRecordRepository.delete(
            record
        )

        return True

    # =========================================================
    # GET BY PATIENT
    # =========================================================

    @staticmethod
    def get_by_patient(patient_id):

        return MedicalRecordRepository.get_by_patient(
            patient_id
        )

    # =========================================================
    # GET BY DOCTOR
    # =========================================================

    @staticmethod
    def get_by_doctor(doctor_id):

        return MedicalRecordRepository.get_by_doctor(
            doctor_id
        )