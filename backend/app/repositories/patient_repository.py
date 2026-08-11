from app.extensions import db
from app.models.patient import Patient


class PatientRepository:

    # =========================================================
    # CREATE PATIENT
    # =========================================================

    @staticmethod
    def create(patient):

        db.session.add(patient)
        db.session.commit()

        return patient

    # =========================================================
    # GET ALL PATIENTS
    # =========================================================

    @staticmethod
    def get_all():

        return Patient.query.all()

    # =========================================================
    # GET PATIENT BY ID
    # =========================================================

    @staticmethod
    def get_by_id(patient_id):

        return Patient.query.get(patient_id)

    # =========================================================
    # GET PATIENT BY EMAIL
    # =========================================================

    @staticmethod
    def get_by_email(email):

        return Patient.query.filter_by(
            email=email
        ).first()

    # =========================================================
    # GET PATIENT BY PHONE
    # =========================================================

    @staticmethod
    def get_by_phone(phone):

        return Patient.query.filter_by(
            phone=phone
        ).first()

    # =========================================================
    # UPDATE PATIENT
    # =========================================================

    @staticmethod
    def update(patient, data):

        for key, value in data.items():

            # Never allow ID to be changed
            if key == "id":
                continue

            # Never allow created_at to be changed
            if key == "created_at":
                continue

            # Prevent updating unknown model attributes
            if not hasattr(patient, key):
                continue

            setattr(
                patient,
                key,
                value
            )

        db.session.commit()

        return patient

    # =========================================================
    # DELETE PATIENT
    # =========================================================

    @staticmethod
    def delete(patient):

        db.session.delete(patient)
        db.session.commit()