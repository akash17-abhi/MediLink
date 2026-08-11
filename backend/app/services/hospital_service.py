from app.extensions import db
from app.models.hospital import Hospital
from app.models.user import User


class HospitalService:

    # =========================================================
    # CREATE HOSPITAL
    # =========================================================

    @staticmethod
    def create_hospital(data):

        # -----------------------------------------------------
        # Check duplicate hospital email
        # -----------------------------------------------------

        existing_email = Hospital.query.filter_by(
            email=data["email"]
        ).first()

        if existing_email:
            return None, "Hospital email already exists."

        # -----------------------------------------------------
        # Check duplicate registration number
        # -----------------------------------------------------

        existing_registration = Hospital.query.filter_by(
            registration_number=data["registration_number"]
        ).first()

        if existing_registration:
            return None, "Registration number already exists."

        # -----------------------------------------------------
        # Create hospital
        # -----------------------------------------------------

        hospital = Hospital(**data)

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

        return Hospital.query.get(hospital_id)

    # =========================================================
    # UPDATE HOSPITAL
    # =========================================================

    @staticmethod
    def update_hospital(hospital, data):

        # -----------------------------------------------------
        # Fields that must NOT be changed through the normal
        # hospital update endpoint.
        #
        # user_id is handled separately by:
        # assign_hospital_to_user()
        # unassign_hospital_from_user()
        # -----------------------------------------------------

        protected_fields = {
            "id",
            "user_id",
            "created_at",
            "updated_at"
        }

        # -----------------------------------------------------
        # Update allowed fields only
        # -----------------------------------------------------

        for key, value in data.items():

            if key in protected_fields:
                continue

            # Prevent updating fields that do not exist
            # on the Hospital model.
            if not hasattr(hospital, key):
                continue

            setattr(
                hospital,
                key,
                value
            )

        # -----------------------------------------------------
        # Save changes
        # -----------------------------------------------------

        db.session.commit()

        return hospital

    # =========================================================
    # DELETE HOSPITAL
    # =========================================================

    @staticmethod
    def delete_hospital(hospital):

        db.session.delete(hospital)

        db.session.commit()

    # =========================================================
    # ASSIGN HOSPITAL TO USER
    # =========================================================

    @staticmethod
    def assign_hospital_to_user(
        hospital_id,
        user_id
    ):

        # -----------------------------------------------------
        # Find hospital
        # -----------------------------------------------------

        hospital = Hospital.query.get(
            hospital_id
        )

        if not hospital:

            return None, "Hospital not found."

        # -----------------------------------------------------
        # Find user
        # -----------------------------------------------------

        user = User.query.get(
            user_id
        )

        if not user:

            return None, "User not found."

        # -----------------------------------------------------
        # Check whether this user already owns another hospital
        # -----------------------------------------------------

        existing_hospital = Hospital.query.filter(
            Hospital.user_id == user_id,
            Hospital.id != hospital_id
        ).first()

        if existing_hospital:

            return (
                None,
                "This user is already assigned to another hospital."
            )

        # -----------------------------------------------------
        # Check whether this hospital belongs to another user
        # -----------------------------------------------------

        if (
            hospital.user_id is not None
            and hospital.user_id != user_id
        ):

            return (
                None,
                "This hospital is already assigned to another user."
            )

        # -----------------------------------------------------
        # Assign hospital to user
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Find hospital
        # -----------------------------------------------------

        hospital = Hospital.query.get(
            hospital_id
        )

        if not hospital:

            return None, "Hospital not found."

        # -----------------------------------------------------
        # Check whether hospital is assigned
        # -----------------------------------------------------

        if hospital.user_id is None:

            return (
                None,
                "This hospital is not assigned to any user."
            )

        # -----------------------------------------------------
        # Remove ownership
        # -----------------------------------------------------

        hospital.user_id = None

        db.session.commit()

        return hospital, None