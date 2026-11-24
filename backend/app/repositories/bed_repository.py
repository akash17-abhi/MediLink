from app.extensions import db
from app.models.bed import Bed


class BedRepository:
    """Repository layer for Bed database operations."""

    # =========================================================
    # CREATE
    # =========================================================

    @staticmethod
    def create(data):
        bed = Bed(**data)

        db.session.add(bed)
        db.session.commit()

        return bed

    # =========================================================
    # GET BY ID
    # =========================================================

    @staticmethod
    def get_by_id(bed_id):
        return db.session.get(Bed, bed_id)

    # =========================================================
    # GET ALL
    # =========================================================

    @staticmethod
    def get_all():
        return (
            Bed.query
            .order_by(Bed.id.desc())
            .all()
        )

    # =========================================================
    # GET BY HOSPITAL
    # =========================================================

    @staticmethod
    def get_by_hospital(hospital_id):
        return (
            Bed.query
            .filter_by(hospital_id=hospital_id)
            .order_by(Bed.id.asc())
            .all()
        )

    # =========================================================
    # GET AVAILABLE BEDS
    # =========================================================

    @staticmethod
    def get_available():
        return (
            Bed.query
            .filter_by(status="Available")
            .order_by(Bed.id.asc())
            .all()
        )

    # =========================================================
    # GET AVAILABLE BEDS BY HOSPITAL
    # =========================================================

    @staticmethod
    def get_available_by_hospital(hospital_id):
        return (
            Bed.query
            .filter_by(
                hospital_id=hospital_id,
                status="Available"
            )
            .order_by(Bed.id.asc())
            .all()
        )

    # =========================================================
    # GET AVAILABLE BEDS BY TYPE
    # =========================================================

    @staticmethod
    def get_available_by_type(bed_type):
        return (
            Bed.query
            .filter_by(
                bed_type=bed_type,
                status="Available"
            )
            .order_by(Bed.id.asc())
            .all()
        )

    # =========================================================
    # GET BEDS BY TYPE
    # =========================================================

    @staticmethod
    def get_by_type(bed_type):
        return (
            Bed.query
            .filter_by(bed_type=bed_type)
            .order_by(Bed.id.asc())
            .all()
        )

    # =========================================================
    # UPDATE
    # =========================================================

    @staticmethod
    def update(bed, data):
        for key, value in data.items():
            if hasattr(bed, key):
                setattr(bed, key, value)

        db.session.commit()

        return bed

    # =========================================================
    # DELETE
    # =========================================================

    @staticmethod
    def delete(bed):
        db.session.delete(bed)
        db.session.commit()

    # =========================================================
    # ASSIGN PATIENT
    # =========================================================

    @staticmethod
    def assign_patient(bed, patient_id):
        bed.patient_id = patient_id
        bed.status = "Occupied"

        db.session.commit()

        return bed

    # =========================================================
    # RELEASE BED
    # =========================================================

    @staticmethod
    def release_bed(bed):
        bed.patient_id = None
        bed.status = "Available"

        db.session.commit()

        return bed

    # =========================================================
    # UPDATE STATUS
    # =========================================================

    @staticmethod
    def update_status(bed, status):
        bed.status = status

        # If bed becomes available, remove patient assignment.
        if status == "Available":
            bed.patient_id = None

        db.session.commit()

        return bed

    # =========================================================
    # COUNT ALL BEDS
    # =========================================================

    @staticmethod
    def count_all():
        return Bed.query.count()

    # =========================================================
    # COUNT BY HOSPITAL
    # =========================================================

    @staticmethod
    def count_by_hospital(hospital_id):
        return (
            Bed.query
            .filter_by(hospital_id=hospital_id)
            .count()
        )

    # =========================================================
    # COUNT AVAILABLE
    # =========================================================

    @staticmethod
    def count_available():
        return (
            Bed.query
            .filter_by(status="Available")
            .count()
        )

    # =========================================================
    # COUNT AVAILABLE BY HOSPITAL
    # =========================================================

    @staticmethod
    def count_available_by_hospital(hospital_id):
        return (
            Bed.query
            .filter_by(
                hospital_id=hospital_id,
                status="Available"
            )
            .count()
        )

    # =========================================================
    # COUNT BY STATUS
    # =========================================================

    @staticmethod
    def count_by_status(status):
        return (
            Bed.query
            .filter_by(status=status)
            .count()
        )

    # =========================================================
    # COUNT BY TYPE
    # =========================================================

    @staticmethod
    def count_by_type(bed_type):
        return (
            Bed.query
            .filter_by(bed_type=bed_type)
            .count()
        )

    # =========================================================
    # COUNT BY TYPE + HOSPITAL
    # =========================================================

    @staticmethod
    def count_by_type_and_hospital(
        bed_type,
        hospital_id
    ):
        return (
            Bed.query
            .filter_by(
                bed_type=bed_type,
                hospital_id=hospital_id
            )
            .count()
        )

    # =========================================================
    # COUNT AVAILABLE BY TYPE + HOSPITAL
    # =========================================================

    @staticmethod
    def count_available_by_type_and_hospital(
        bed_type,
        hospital_id
    ):
        return (
            Bed.query
            .filter_by(
                bed_type=bed_type,
                hospital_id=hospital_id,
                status="Available"
            )
            .count()
        )