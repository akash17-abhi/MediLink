from app.extensions import db
from app.models.hospital import Hospital


class HospitalRepository:


    # =========================================================
    # CREATE HOSPITAL
    # =========================================================

    @staticmethod
    def create(data):

        hospital = Hospital(
            **data
        )

        db.session.add(
            hospital
        )

        db.session.commit()

        return hospital


    # =========================================================
    # GET ALL HOSPITALS
    # =========================================================

    @staticmethod
    def get_all():

        return Hospital.query.all()


    # =========================================================
    # GET HOSPITAL BY ID
    # =========================================================

    @staticmethod
    def get_by_id(hospital_id):

        return db.session.get(
            Hospital,
            hospital_id
        )


    # =========================================================
    # GET HOSPITAL BY EMAIL
    # =========================================================

    @staticmethod
    def get_by_email(email):

        return Hospital.query.filter_by(
            email=email
        ).first()


    # =========================================================
    # GET HOSPITAL BY REGISTRATION NUMBER
    # =========================================================

    @staticmethod
    def get_by_registration_number(
        registration_number
    ):

        return Hospital.query.filter_by(
            registration_number=registration_number
        ).first()


    # =========================================================
    # UPDATE HOSPITAL
    # =========================================================

    @staticmethod
    def update(
        hospital,
        data
    ):

        for key, value in data.items():

            if hasattr(
                hospital,
                key
            ):

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
    def delete(hospital):

        db.session.delete(
            hospital
        )

        db.session.commit()

        return True