from app.models.doctor import Doctor
from app.models.hospital import Hospital

from app.repositories.doctor_repository import DoctorRepository


class DoctorService:

    # =========================================================
    # CREATE DOCTOR
    # =========================================================

    @staticmethod
    def create(data):

        # -----------------------------------------------------
        # Check duplicate doctor email
        # -----------------------------------------------------

        existing = DoctorRepository.get_by_email(
            data["email"]
        )

        if existing:
            return None, "Doctor email already exists"

        # -----------------------------------------------------
        # Check hospital exists
        # -----------------------------------------------------

        hospital = Hospital.query.get(
            data["hospital_id"]
        )

        if not hospital:
            return None, "Hospital not found"

        # -----------------------------------------------------
        # Check hospital is active
        # -----------------------------------------------------

        if not hospital.is_active:
            return None, "Hospital is not active"

        # -----------------------------------------------------
        # Create doctor
        # -----------------------------------------------------

        doctor = Doctor(
            full_name=data["full_name"],
            email=data["email"],
            phone=data.get("phone"),
            specialization=data["specialization"],
            qualification=data.get("qualification"),
            experience=data.get("experience", 0),
            consultation_fee=data.get("consultation_fee", 0),
            profile_photo=data.get("profile_photo"),
            hospital_id=data["hospital_id"],
            is_active=True
        )

        # -----------------------------------------------------
        # Save doctor
        # -----------------------------------------------------

        DoctorRepository.create(doctor)

        return doctor, None

    # =========================================================
    # GET ALL DOCTORS
    # =========================================================

    @staticmethod
    def get_all():

        return DoctorRepository.get_all()

    # =========================================================
    # GET DOCTOR BY ID
    # =========================================================

    @staticmethod
    def get_by_id(doctor_id):

        return DoctorRepository.get_by_id(
            doctor_id
        )

    # =========================================================
    # UPDATE DOCTOR
    # =========================================================

    @staticmethod
    def update(
        doctor_id,
        data
    ):

        doctor = DoctorRepository.get_by_id(
            doctor_id
        )

        if not doctor:
            return None, "Doctor not found"

        # -----------------------------------------------------
        # Fields that cannot be modified normally
        # -----------------------------------------------------

        protected_fields = {
            "id",
            "created_at",
            "updated_at"
        }

        # -----------------------------------------------------
        # Fields that are allowed to be updated
        # -----------------------------------------------------

        allowed_fields = {
            "full_name",
            "email",
            "phone",
            "specialization",
            "qualification",
            "experience",
            "consultation_fee",
            "profile_photo",
            "is_active",
            "hospital_id"
        }

        # -----------------------------------------------------
        # Check email change
        # -----------------------------------------------------

        if "email" in data:

            existing = DoctorRepository.get_by_email(
                data["email"]
            )

            if existing and existing.id != doctor.id:
                return None, "Doctor email already exists"

        # -----------------------------------------------------
        # Check hospital change
        # -----------------------------------------------------

        if "hospital_id" in data:

            hospital = Hospital.query.get(
                data["hospital_id"]
            )

            if not hospital:
                return None, "Hospital not found"

            if not hospital.is_active:
                return None, "Hospital is not active"

        # -----------------------------------------------------
        # Update allowed fields only
        # -----------------------------------------------------

        for key, value in data.items():

            if key in protected_fields:
                continue

            if key not in allowed_fields:
                continue

            setattr(
                doctor,
                key,
                value
            )

        # -----------------------------------------------------
        # Save changes
        # -----------------------------------------------------

        DoctorRepository.update()

        return doctor, None

    # =========================================================
    # DELETE DOCTOR
    # =========================================================

    @staticmethod
    def delete(doctor_id):

        doctor = DoctorRepository.get_by_id(
            doctor_id
        )

        if not doctor:
            return False

        DoctorRepository.delete(
            doctor
        )

        return True