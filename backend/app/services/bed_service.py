from app.repositories.bed_repository import BedRepository
from app.models.hospital import Hospital
from app.models.patient import Patient


class BedService:
    """Business logic layer for bed management."""

    # =========================================================
    # CREATE BED
    # =========================================================

    @staticmethod
    def create_bed(data):

        hospital_id = data.get("hospital_id")

        # -----------------------------------------------------
        # Verify hospital exists
        # -----------------------------------------------------

        hospital = Hospital.query.get(hospital_id)

        if not hospital:
            return None, "Hospital not found"

        # -----------------------------------------------------
        # Check duplicate bed number within hospital
        # -----------------------------------------------------

        existing_beds = BedRepository.get_by_hospital(
            hospital_id
        )

        for bed in existing_beds:
            if bed.bed_number == data.get("bed_number"):
                return None, "Bed number already exists in this hospital"

        # -----------------------------------------------------
        # Validate patient assignment
        # -----------------------------------------------------

        patient_id = data.get("patient_id")

        if patient_id:

            patient = Patient.query.get(patient_id)

            if not patient:
                return None, "Patient not found"

            if data.get("status", "Available") != "Occupied":
                return None, (
                    "A patient can only be assigned to an occupied bed"
                )

        # -----------------------------------------------------
        # Create bed
        # -----------------------------------------------------

        bed = BedRepository.create(data)

        return bed, None

    # =========================================================
    # GET BED
    # =========================================================

    @staticmethod
    def get_bed(bed_id):

        bed = BedRepository.get_by_id(bed_id)

        if not bed:
            return None, "Bed not found"

        return bed, None

    # =========================================================
    # GET ALL BEDS
    # =========================================================

    @staticmethod
    def get_all_beds():

        beds = BedRepository.get_all()

        return beds, None

    # =========================================================
    # GET HOSPITAL BEDS
    # =========================================================

    @staticmethod
    def get_hospital_beds(hospital_id):

        hospital = Hospital.query.get(hospital_id)

        if not hospital:
            return None, "Hospital not found"

        beds = BedRepository.get_by_hospital(
            hospital_id
        )

        return beds, None

    # =========================================================
    # GET AVAILABLE BEDS
    # =========================================================

    @staticmethod
    def get_available_beds():

        beds = BedRepository.get_available()

        return beds, None

    # =========================================================
    # GET AVAILABLE BEDS BY HOSPITAL
    # =========================================================

    @staticmethod
    def get_available_hospital_beds(hospital_id):

        hospital = Hospital.query.get(hospital_id)

        if not hospital:
            return None, "Hospital not found"

        beds = BedRepository.get_available_by_hospital(
            hospital_id
        )

        return beds, None

    # =========================================================
    # GET AVAILABLE BEDS BY TYPE
    # =========================================================

    @staticmethod
    def get_available_beds_by_type(
        bed_type,
        hospital_id=None
    ):

        if hospital_id:

            hospital = Hospital.query.get(hospital_id)

            if not hospital:
                return None, "Hospital not found"

            beds = BedRepository.get_available_by_type(
                bed_type
            )

            beds = [
                bed
                for bed in beds
                if bed.hospital_id == hospital_id
            ]

        else:

            beds = BedRepository.get_available_by_type(
                bed_type
            )

        return beds, None

    # =========================================================
    # UPDATE BED
    # =========================================================

    @staticmethod
    def update_bed(bed_id, data):

        bed = BedRepository.get_by_id(bed_id)

        if not bed:
            return None, "Bed not found"

        # -----------------------------------------------------
        # Check duplicate bed number
        # -----------------------------------------------------

        if "bed_number" in data:

            hospital_beds = BedRepository.get_by_hospital(
                bed.hospital_id
            )

            for existing_bed in hospital_beds:

                if (
                    existing_bed.id != bed.id
                    and existing_bed.bed_number
                    == data["bed_number"]
                ):
                    return None, (
                        "Bed number already exists in this hospital"
                    )

        # -----------------------------------------------------
        # Validate patient
        # -----------------------------------------------------

        if "patient_id" in data:

            patient_id = data["patient_id"]

            if patient_id:

                patient = Patient.query.get(patient_id)

                if not patient:
                    return None, "Patient not found"

        # -----------------------------------------------------
        # Status validation
        # -----------------------------------------------------

        if "status" in data:

            status = data["status"]

            if status == "Occupied":

                patient_id = data.get(
                    "patient_id",
                    bed.patient_id
                )

                if not patient_id:
                    return None, (
                        "An occupied bed must have a patient assigned"
                    )

            elif status == "Available":

                data["patient_id"] = None

        # -----------------------------------------------------
        # Update
        # -----------------------------------------------------

        bed = BedRepository.update(
            bed,
            data
        )

        return bed, None

    # =========================================================
    # DELETE BED
    # =========================================================

    @staticmethod
    def delete_bed(bed_id):

        bed = BedRepository.get_by_id(bed_id)

        if not bed:
            return None, "Bed not found"

        # -----------------------------------------------------
        # Don't delete occupied bed
        # -----------------------------------------------------

        if bed.status == "Occupied":

            return None, (
                "Occupied beds cannot be deleted"
            )

        BedRepository.delete(bed)

        return True, None

    # =========================================================
    # ASSIGN PATIENT
    # =========================================================

    @staticmethod
    def assign_patient(
        bed_id,
        patient_id
    ):

        bed = BedRepository.get_by_id(bed_id)

        if not bed:
            return None, "Bed not found"

        # -----------------------------------------------------
        # Bed must be available
        # -----------------------------------------------------

        if bed.status != "Available":

            return None, (
                f"Bed is currently {bed.status}"
            )

        # -----------------------------------------------------
        # Patient must exist
        # -----------------------------------------------------

        patient = Patient.query.get(patient_id)

        if not patient:
            return None, "Patient not found"

        # -----------------------------------------------------
        # Check patient isn't already assigned
        # -----------------------------------------------------

        existing_beds = BedRepository.get_by_hospital(
            bed.hospital_id
        )

        for existing_bed in existing_beds:

            if (
                existing_bed.patient_id == patient_id
                and existing_bed.id != bed.id
                and existing_bed.status == "Occupied"
            ):

                return None, (
                    "Patient is already assigned to another bed"
                )

        # -----------------------------------------------------
        # Assign
        # -----------------------------------------------------

        bed = BedRepository.assign_patient(
            bed,
            patient_id
        )

        return bed, None

    # =========================================================
    # RELEASE BED
    # =========================================================

    @staticmethod
    def release_bed(bed_id):

        bed = BedRepository.get_by_id(bed_id)

        if not bed:
            return None, "Bed not found"

        if bed.status != "Occupied":

            return None, (
                "Only occupied beds can be released"
            )

        bed = BedRepository.release_bed(
            bed
        )

        return bed, None

    # =========================================================
    # UPDATE STATUS
    # =========================================================

    @staticmethod
    def update_status(
        bed_id,
        status
    ):

        bed = BedRepository.get_by_id(bed_id)

        if not bed:
            return None, "Bed not found"

        # -----------------------------------------------------
        # Occupied requires patient
        # -----------------------------------------------------

        if status == "Occupied" and not bed.patient_id:

            return None, (
                "An occupied bed must have a patient assigned"
            )

        # -----------------------------------------------------
        # Available automatically releases patient
        # -----------------------------------------------------

        bed = BedRepository.update_status(
            bed,
            status
        )

        return bed, None

    # =========================================================
    # BED STATISTICS
    # =========================================================

    @staticmethod
    def get_statistics(
        hospital_id=None
    ):

        if hospital_id:

            hospital = Hospital.query.get(
                hospital_id
            )

            if not hospital:
                return None, "Hospital not found"

            total = BedRepository.count_by_hospital(
                hospital_id
            )

            available = BedRepository.count_available_by_hospital(
                hospital_id
            )

            occupied = sum(
                1
                for bed in BedRepository.get_by_hospital(
                    hospital_id
                )
                if bed.status == "Occupied"
            )

            reserved = sum(
                1
                for bed in BedRepository.get_by_hospital(
                    hospital_id
                )
                if bed.status == "Reserved"
            )

            maintenance = sum(
                1
                for bed in BedRepository.get_by_hospital(
                    hospital_id
                )
                if bed.status == "Maintenance"
            )

            blocked = sum(
                1
                for bed in BedRepository.get_by_hospital(
                    hospital_id
                )
                if bed.status == "Blocked"
            )

        else:

            total = BedRepository.count_all()

            available = BedRepository.count_available()

            occupied = BedRepository.count_by_status(
                "Occupied"
            )

            reserved = BedRepository.count_by_status(
                "Reserved"
            )

            maintenance = BedRepository.count_by_status(
                "Maintenance"
            )

            blocked = BedRepository.count_by_status(
                "Blocked"
            )

        return {
            "total_beds": total,
            "available_beds": available,
            "occupied_beds": occupied,
            "reserved_beds": reserved,
            "maintenance_beds": maintenance,
            "blocked_beds": blocked,
        }, None