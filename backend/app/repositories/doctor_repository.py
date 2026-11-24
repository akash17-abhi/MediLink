from app.extensions import db
from app.models.doctor import Doctor


class DoctorRepository:


    # =========================================================
    # CREATE DOCTOR
    # =========================================================

    @staticmethod
    def create(doctor):

        db.session.add(doctor)

        db.session.commit()

        return doctor


    # =========================================================
    # GET ALL DOCTORS
    # =========================================================

    @staticmethod
    def get_all():

        return Doctor.query.all()


    # =========================================================
    # GET DOCTOR BY ID
    # =========================================================

    @staticmethod
    def get_by_id(doctor_id):

        return db.session.get(
            Doctor,
            doctor_id
        )


    # =========================================================
    # GET DOCTOR BY EMAIL
    # =========================================================

    @staticmethod
    def get_by_email(email):

        return Doctor.query.filter_by(
            email=email
        ).first()


    # =========================================================
    # UPDATE DOCTOR
    # =========================================================

    @staticmethod
    def update(doctor):

        db.session.commit()

        return doctor


    # =========================================================
    # DELETE DOCTOR
    # =========================================================

    @staticmethod
    def delete(doctor):

        db.session.delete(doctor)

        db.session.commit()

        return True