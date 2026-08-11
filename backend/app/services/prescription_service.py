from app.models.prescription import Prescription

from app.repositories.prescription_repository import (
    PrescriptionRepository
)

from app.repositories.patient_repository import (
    PatientRepository
)

from app.repositories.doctor_repository import (
    DoctorRepository
)

from app.repositories.medical_record_repository import (
    MedicalRecordRepository
)


class PrescriptionService:

    # =========================================================
    # CREATE PRESCRIPTION
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
            return None, "Patient not found"

        # -----------------------------------------------------
        # Check doctor
        # -----------------------------------------------------

        doctor = DoctorRepository.get_by_id(
            data["doctor_id"]
        )

        if not doctor:
            return None, "Doctor not found"

        # -----------------------------------------------------
        # Check medical record
        # -----------------------------------------------------

        record = MedicalRecordRepository.get_by_id(
            data["medical_record_id"]
        )

        if not record:
            return None, "Medical Record not found"

        # -----------------------------------------------------
        # Verify medical record belongs to patient
        # -----------------------------------------------------

        if record.patient_id != data["patient_id"]:

            return (
                None,
                "Medical record does not belong to this patient"
            )

        # -----------------------------------------------------
        # Verify medical record belongs to doctor
        # -----------------------------------------------------

        if record.doctor_id != data["doctor_id"]:

            return (
                None,
                "Medical record does not belong to this doctor"
            )

        # =====================================================
        # CREATE PRESCRIPTION
        # =====================================================

        prescription = Prescription(

            medical_record_id=data[
                "medical_record_id"
            ],

            patient_id=data[
                "patient_id"
            ],

            doctor_id=data[
                "doctor_id"
            ],

            medicines=data[
                "medicines"
            ],

            dosage=data.get(
                "dosage"
            ),

            duration=data.get(
                "duration"
            ),

            instructions=data.get(
                "instructions"
            )
        )

        PrescriptionRepository.create(
            prescription
        )

        return prescription, None

    # =========================================================
    # GET ALL
    # =========================================================

    @staticmethod
    def get_all():

        return PrescriptionRepository.get_all()

    # =========================================================
    # GET BY ID
    # =========================================================

    @staticmethod
    def get_by_id(prescription_id):

        return PrescriptionRepository.get_by_id(
            prescription_id
        )

    # =========================================================
    # UPDATE
    # =========================================================

    @staticmethod
    def update(prescription_id, data):

        prescription = (
            PrescriptionRepository.get_by_id(
                prescription_id
            )
        )

        if not prescription:

            return (
                None,
                "Prescription not found"
            )

        # -----------------------------------------------------
        # Validate patient if changed
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
        # Validate doctor if changed
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
        # Validate medical record if changed
        # -----------------------------------------------------

        if "medical_record_id" in data:

            record = MedicalRecordRepository.get_by_id(
                data["medical_record_id"]
            )

            if not record:

                return (
                    None,
                    "Medical Record not found"
                )

            new_patient_id = data.get(
                "patient_id",
                prescription.patient_id
            )

            new_doctor_id = data.get(
                "doctor_id",
                prescription.doctor_id
            )

            if record.patient_id != new_patient_id:

                return (
                    None,
                    "Medical record does not belong to this patient"
                )

            if record.doctor_id != new_doctor_id:

                return (
                    None,
                    "Medical record does not belong to this doctor"
                )

        # =====================================================
        # ALLOWED UPDATE FIELDS
        # =====================================================

        allowed_fields = [
            "medical_record_id",
            "patient_id",
            "doctor_id",
            "medicines",
            "dosage",
            "duration",
            "instructions"
        ]

        for key, value in data.items():

            if key in allowed_fields:

                setattr(
                    prescription,
                    key,
                    value
                )

        # =====================================================
        # SAVE
        # =====================================================

        PrescriptionRepository.update()

        return prescription, None

    # =========================================================
    # DELETE
    # =========================================================

    @staticmethod
    def delete(prescription_id):

        prescription = (
            PrescriptionRepository.get_by_id(
                prescription_id
            )
        )

        if not prescription:

            return False

        PrescriptionRepository.delete(
            prescription
        )

        return True

    # =========================================================
    # GET BY PATIENT
    # =========================================================

    @staticmethod
    def get_by_patient(patient_id):

        return PrescriptionRepository.get_by_patient(
            patient_id
        )

    # =========================================================
    # GET BY DOCTOR
    # =========================================================

    @staticmethod
    def get_by_doctor(doctor_id):

        return PrescriptionRepository.get_by_doctor(
            doctor_id
        )