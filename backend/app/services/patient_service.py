from datetime import datetime

from app.models.patient import Patient
from app.repositories.patient_repository import PatientRepository


class PatientService:

    # =========================================================
    # CREATE PATIENT
    # =========================================================

    @staticmethod
    def create(data):

        # -----------------------------------------------------
        # Check duplicate email
        # -----------------------------------------------------

        existing = PatientRepository.get_by_email(
            data["email"]
        )

        if existing:

            return (
                None,
                "Patient email already exists"
            )

        # -----------------------------------------------------
        # Check duplicate phone
        # -----------------------------------------------------

        existing_phone = PatientRepository.get_by_phone(
            data["phone"]
        )

        if existing_phone:

            return (
                None,
                "Patient phone already exists"
            )

        # -----------------------------------------------------
        # Convert date of birth
        # -----------------------------------------------------

        date_of_birth = data["date_of_birth"]

        if isinstance(date_of_birth, str):

            date_of_birth = datetime.strptime(
                date_of_birth,
                "%Y-%m-%d"
            ).date()

        # -----------------------------------------------------
        # Convert insurance validity date
        # -----------------------------------------------------

        insurance_valid_until = data.get(
            "insurance_valid_until"
        )

        if (
            insurance_valid_until
            and isinstance(
                insurance_valid_until,
                str
            )
        ):

            insurance_valid_until = datetime.strptime(
                insurance_valid_until,
                "%Y-%m-%d"
            ).date()

        # -----------------------------------------------------
        # Create patient
        # -----------------------------------------------------

        patient = Patient(

            # Personal information
            full_name=data["full_name"],
            email=data["email"],
            phone=data["phone"],
            gender=data["gender"],
            date_of_birth=date_of_birth,

            # Medical information
            blood_group=data.get("blood_group"),
            allergies=data.get("allergies"),
            chronic_conditions=data.get(
                "chronic_conditions"
            ),
            current_medications=data.get(
                "current_medications"
            ),
            medical_history=data.get(
                "medical_history"
            ),

            # Address
            address=data.get("address"),
            city=data.get("city"),
            state=data.get("state"),
            pincode=data.get("pincode"),
            country=data.get(
                "country",
                "India"
            ),

            # Emergency contact
            emergency_contact_name=data.get(
                "emergency_contact_name"
            ),
            emergency_contact_phone=data.get(
                "emergency_contact_phone"
            ),
            emergency_contact_relation=data.get(
                "emergency_contact_relation"
            ),

            # Profile
            profile_photo=data.get(
                "profile_photo"
            ),

            # Insurance
            insurance_provider=data.get(
                "insurance_provider"
            ),
            insurance_policy_number=data.get(
                "insurance_policy_number"
            ),
            insurance_valid_until=insurance_valid_until,

            # User relationship
            user_id=data.get("user_id")
        )

        # -----------------------------------------------------
        # Save
        # -----------------------------------------------------

        PatientRepository.create(patient)

        return patient, None

    # =========================================================
    # GET ALL PATIENTS
    # =========================================================

    @staticmethod
    def get_all():

        return PatientRepository.get_all()

    # =========================================================
    # GET PATIENT BY ID
    # =========================================================

    @staticmethod
    def get_by_id(patient_id):

        return PatientRepository.get_by_id(
            patient_id
        )

    # =========================================================
    # UPDATE PATIENT
    # =========================================================

    @staticmethod
    def update(patient_id, data):

        patient = PatientRepository.get_by_id(
            patient_id
        )

        if not patient:

            return None

        # -----------------------------------------------------
        # Check duplicate email
        # -----------------------------------------------------

        if "email" in data:

            existing = PatientRepository.get_by_email(
                data["email"]
            )

            if (
                existing
                and existing.id != patient.id
            ):

                return (
                    None,
                    "Patient email already exists"
                )

        # -----------------------------------------------------
        # Check duplicate phone
        # -----------------------------------------------------

        if "phone" in data:

            existing_phone = (
                PatientRepository.get_by_phone(
                    data["phone"]
                )
            )

            if (
                existing_phone
                and existing_phone.id != patient.id
            ):

                return (
                    None,
                    "Patient phone already exists"
                )

        # -----------------------------------------------------
        # Convert date of birth
        # -----------------------------------------------------

        if "date_of_birth" in data:

            if isinstance(
                data["date_of_birth"],
                str
            ):

                data["date_of_birth"] = (
                    datetime.strptime(
                        data["date_of_birth"],
                        "%Y-%m-%d"
                    ).date()
                )

        # -----------------------------------------------------
        # Convert insurance date
        # -----------------------------------------------------

        if "insurance_valid_until" in data:

            if (
                data["insurance_valid_until"]
                and isinstance(
                    data["insurance_valid_until"],
                    str
                )
            ):

                data["insurance_valid_until"] = (
                    datetime.strptime(
                        data["insurance_valid_until"],
                        "%Y-%m-%d"
                    ).date()
                )

        # -----------------------------------------------------
        # Prevent protected fields
        # -----------------------------------------------------

        protected_fields = {
            "id",
            "created_at",
            "updated_at"
        }

        clean_data = {
            key: value
            for key, value in data.items()
            if key not in protected_fields
        }

        # -----------------------------------------------------
        # Update
        # -----------------------------------------------------

        patient = PatientRepository.update(
            patient,
            clean_data
        )

        return patient, None

    # =========================================================
    # DELETE PATIENT
    # =========================================================

    @staticmethod
    def delete(patient_id):

        patient = PatientRepository.get_by_id(
            patient_id
        )

        if not patient:

            return False

        PatientRepository.delete(patient)

        return True