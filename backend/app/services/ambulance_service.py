from app.models.ambulance import Ambulance

from app.repositories.ambulance_repository import (
    AmbulanceRepository
)

from app.repositories.hospital_repository import (
    HospitalRepository
)


class AmbulanceService:

    # =========================================================
    # CREATE AMBULANCE
    # =========================================================

    @staticmethod
    def create(data):

        # -----------------------------------------------------
        # Check hospital
        # -----------------------------------------------------

        hospital = HospitalRepository.get_by_id(
            data["hospital_id"]
        )

        if not hospital:
            return None, "Hospital not found"

        # -----------------------------------------------------
        # Check duplicate registration number
        # -----------------------------------------------------

        existing = (
            AmbulanceRepository.get_by_registration_number(
                data["registration_number"]
            )
        )

        if existing:
            return (
                None,
                "Ambulance with this registration number already exists"
            )

        # =====================================================
        # CREATE AMBULANCE
        # =====================================================

        ambulance = Ambulance(

            hospital_id=data[
                "hospital_id"
            ],

            registration_number=data[
                "registration_number"
            ],

            ambulance_type=data[
                "ambulance_type"
            ],

            driver_name=data[
                "driver_name"
            ],

            driver_phone=data[
                "driver_phone"
            ],

            current_location=data.get(
                "current_location"
            ),

            availability_status=data.get(
                "availability_status",
                "Available"
            ),

            emergency_status=data.get(
                "emergency_status",
                "Normal"
            )
        )

        AmbulanceRepository.create(
            ambulance
        )

        return ambulance, None

    # =========================================================
    # GET ALL
    # =========================================================

    @staticmethod
    def get_all():

        return AmbulanceRepository.get_all()

    # =========================================================
    # GET BY ID
    # =========================================================

    @staticmethod
    def get_by_id(ambulance_id):

        return AmbulanceRepository.get_by_id(
            ambulance_id
        )

    # =========================================================
    # GET BY HOSPITAL
    # =========================================================

    @staticmethod
    def get_by_hospital(hospital_id):

        return AmbulanceRepository.get_by_hospital(
            hospital_id
        )

    # =========================================================
    # GET AVAILABLE AMBULANCES
    # =========================================================

    @staticmethod
    def get_available():

        return AmbulanceRepository.get_available()

    # =========================================================
    # GET AVAILABLE AMBULANCES BY HOSPITAL
    # =========================================================

    @staticmethod
    def get_available_by_hospital(hospital_id):

        return (
            AmbulanceRepository
            .get_available_by_hospital(
                hospital_id
            )
        )

    # =========================================================
    # GET EMERGENCY AVAILABLE AMBULANCES
    # =========================================================

    @staticmethod
    def get_emergency_available():

        return (
            AmbulanceRepository
            .get_emergency_available()
        )

    # =========================================================
    # UPDATE
    # =========================================================

    @staticmethod
    def update(ambulance_id, data):

        ambulance = AmbulanceRepository.get_by_id(
            ambulance_id
        )

        if not ambulance:
            return None, "Ambulance not found"

        # -----------------------------------------------------
        # Validate hospital if changed
        # -----------------------------------------------------

        if "hospital_id" in data:

            hospital = HospitalRepository.get_by_id(
                data["hospital_id"]
            )

            if not hospital:
                return None, "Hospital not found"

        # -----------------------------------------------------
        # Check registration number if changed
        # -----------------------------------------------------

        if "registration_number" in data:

            if (
                data["registration_number"]
                != ambulance.registration_number
            ):

                existing = (
                    AmbulanceRepository
                    .get_by_registration_number(
                        data["registration_number"]
                    )
                )

                if existing:

                    return (
                        None,
                        "Ambulance with this registration number already exists"
                    )

        # =====================================================
        # ALLOWED UPDATE FIELDS
        # =====================================================

        allowed_fields = [

            "hospital_id",

            "registration_number",

            "ambulance_type",

            "driver_name",

            "driver_phone",

            "current_location",

            "availability_status",

            "emergency_status"
        ]

        # =====================================================
        # UPDATE FIELDS
        # =====================================================

        for key, value in data.items():

            if key in allowed_fields:

                setattr(
                    ambulance,
                    key,
                    value
                )

        # =====================================================
        # SAVE
        # =====================================================

        AmbulanceRepository.update()

        return ambulance, None

    # =========================================================
    # DELETE
    # =========================================================

    @staticmethod
    def delete(ambulance_id):

        ambulance = AmbulanceRepository.get_by_id(
            ambulance_id
        )

        if not ambulance:
            return False

        AmbulanceRepository.delete(
            ambulance
        )

        return True