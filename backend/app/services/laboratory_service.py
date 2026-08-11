from app.models.laboratory import Laboratory

from app.repositories.patient_repository import PatientRepository
from app.repositories.doctor_repository import DoctorRepository
from app.repositories.hospital_repository import HospitalRepository
from app.repositories.laboratory_repository import LaboratoryRepository


class LaboratoryService:

    @staticmethod
    def create(data):

        # =========================================================
        # VERIFY PATIENT
        # =========================================================

        patient = PatientRepository.get_by_id(
            data["patient_id"]
        )

        if not patient:
            return None, "Patient not found"

        # =========================================================
        # VERIFY DOCTOR
        # =========================================================

        doctor = DoctorRepository.get_by_id(
            data["doctor_id"]
        )

        if not doctor:
            return None, "Doctor not found"

        # =========================================================
        # VERIFY HOSPITAL
        # =========================================================

        hospital = HospitalRepository.get_by_id(
            data["hospital_id"]
        )

        if not hospital:
            return None, "Hospital not found"

        # =========================================================
        # CREATE LABORATORY TEST
        # =========================================================

        test = Laboratory(
            patient_id=data["patient_id"],
            doctor_id=data["doctor_id"],
            hospital_id=data["hospital_id"],
            test_name=data["test_name"],
            category=data.get("category"),
            status=data.get("status", "Pending"),
            result=data.get("result"),
            report_file=data.get("report_file")
        )

        LaboratoryRepository.create(test)

        return test, None

    # =============================================================
    # GET ALL
    # =============================================================

    @staticmethod
    def get_all():
        return LaboratoryRepository.get_all()

    # =============================================================
    # GET BY ID
    # =============================================================

    @staticmethod
    def get_by_id(test_id):
        return LaboratoryRepository.get_by_id(test_id)

    # =============================================================
    # UPDATE
    # =============================================================

    @staticmethod
    def update(test_id, data):

        test = LaboratoryRepository.get_by_id(test_id)

        if not test:
            return None

        for key, value in data.items():
            setattr(test, key, value)

        LaboratoryRepository.update()

        return test

    # =============================================================
    # DELETE
    # =============================================================

    @staticmethod
    def delete(test_id):

        test = LaboratoryRepository.get_by_id(test_id)

        if not test:
            return False

        LaboratoryRepository.delete(test)

        return True

    # =============================================================
    # GET BY PATIENT
    # =============================================================

    @staticmethod
    def get_by_patient(patient_id):
        return LaboratoryRepository.get_by_patient(
            patient_id
        )

    # =============================================================
    # GET BY DOCTOR
    # =============================================================

    @staticmethod
    def get_by_doctor(doctor_id):
        return LaboratoryRepository.get_by_doctor(
            doctor_id
        )