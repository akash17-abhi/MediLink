from app.extensions import db

from app.models.hospital import Hospital
from app.models.user import User


class HospitalService:


    # =========================================================
    # CREATE HOSPITAL
    # =========================================================

    @staticmethod
    def create_hospital(data):

        existing_email = Hospital.query.filter_by(
            email=data["email"]
        ).first()

        if existing_email:

            return (
                None,
                "Hospital email already exists."
            )


        existing_registration = Hospital.query.filter_by(
            registration_number=data["registration_number"]
        ).first()

        if existing_registration:

            return (
                None,
                "Registration number already exists."
            )


        hospital = Hospital(
            **data
        )

        db.session.add(hospital)

        db.session.commit()

        return hospital, None


    # =========================================================
    # GET ALL HOSPITALS
    # =========================================================

    @staticmethod
    def get_all_hospitals():

        return Hospital.query.all()


    # =========================================================
    # GET HOSPITAL BY ID
    # =========================================================

    @staticmethod
    def get_hospital(hospital_id):

        return db.session.get(
            Hospital,
            hospital_id
        )


    # =========================================================
    # UPDATE HOSPITAL
    # =========================================================

    @staticmethod
    def update_hospital(
        hospital,
        data
    ):

        protected_fields = {
            "id",
            "user_id",
            "created_at",
            "updated_at"
        }


        for key, value in data.items():

            if key in protected_fields:
                continue

            if not hasattr(
                hospital,
                key
            ):
                continue

            setattr(
                hospital,
                key,
                value
            )


        db.session.commit()

        return hospital


    # =========================================================
    # DELETE HOSPITAL
    # =========================================================

    @staticmethod
    def delete_hospital(hospital):

        db.session.delete(
            hospital
        )

        db.session.commit()


    # =========================================================
    # ASSIGN HOSPITAL TO USER
    # =========================================================

    @staticmethod
    def assign_hospital_to_user(
        hospital_id,
        user_id
    ):

        hospital = db.session.get(
            Hospital,
            hospital_id
        )

        if not hospital:

            return (
                None,
                "Hospital not found."
            )


        user = db.session.get(
            User,
            user_id
        )

        if not user:

            return (
                None,
                "User not found."
            )


        existing_hospital = Hospital.query.filter(
            Hospital.user_id == user_id,
            Hospital.id != hospital_id
        ).first()


        if existing_hospital:

            return (
                None,
                "This user is already assigned to another hospital."
            )


        if (
            hospital.user_id is not None
            and hospital.user_id != user_id
        ):

            return (
                None,
                "This hospital is already assigned to another user."
            )


        hospital.user_id = user_id

        db.session.commit()

        return hospital, None


    # =========================================================
    # UNASSIGN HOSPITAL FROM USER
    # =========================================================

    @staticmethod
    def unassign_hospital_from_user(
        hospital_id
    ):

        hospital = db.session.get(
            Hospital,
            hospital_id
        )

        if not hospital:

            return (
                None,
                "Hospital not found."
            )


        if hospital.user_id is None:

            return (
                None,
                "This hospital is not assigned to any user."
            )


        hospital.user_id = None

        db.session.commit()

        return hospital, None