from app.extensions import db
from app.models.ambulance import Ambulance


class AmbulanceRepository:

    # =========================================================
    # CREATE
    # =========================================================

    @staticmethod
    def create(ambulance):

        db.session.add(ambulance)
        db.session.commit()

        return ambulance

    # =========================================================
    # GET ALL
    # =========================================================

    @staticmethod
    def get_all():

        return Ambulance.query.all()

    # =========================================================
    # GET BY ID
    # =========================================================

    @staticmethod
    def get_by_id(ambulance_id):

        return Ambulance.query.get(ambulance_id)

    # =========================================================
    # GET BY HOSPITAL
    # =========================================================

    @staticmethod
    def get_by_hospital(hospital_id):

        return Ambulance.query.filter_by(
            hospital_id=hospital_id
        ).all()

    # =========================================================
    # GET AVAILABLE AMBULANCES
    # =========================================================

    @staticmethod
    def get_available():

        return Ambulance.query.filter_by(
            availability_status="Available"
        ).all()

    # =========================================================
    # GET AVAILABLE AMBULANCES BY HOSPITAL
    # =========================================================

    @staticmethod
    def get_available_by_hospital(hospital_id):

        return Ambulance.query.filter_by(
            hospital_id=hospital_id,
            availability_status="Available"
        ).all()

    # =========================================================
    # GET EMERGENCY AVAILABLE AMBULANCES
    # =========================================================

    @staticmethod
    def get_emergency_available():

        return Ambulance.query.filter_by(
            availability_status="Available",
            emergency_status="Emergency"
        ).all()

    # =========================================================
    # SEARCH BY REGISTRATION NUMBER
    # =========================================================

    @staticmethod
    def get_by_registration_number(
        registration_number
    ):

        return Ambulance.query.filter_by(
            registration_number=registration_number
        ).first()

    # =========================================================
    # UPDATE
    # =========================================================

    @staticmethod
    def update():

        db.session.commit()

    # =========================================================
    # DELETE
    # =========================================================

    @staticmethod
    def delete(ambulance):

        db.session.delete(ambulance)
        db.session.commit()