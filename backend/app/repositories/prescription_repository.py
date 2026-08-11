from app.extensions import db
from app.models.prescription import Prescription


class PrescriptionRepository:

    @staticmethod
    def create(prescription):
        db.session.add(prescription)
        db.session.commit()
        return prescription

    @staticmethod
    def get_all():
        return Prescription.query.all()

    @staticmethod
    def get_by_id(prescription_id):
        return Prescription.query.get(prescription_id)

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(prescription):
        db.session.delete(prescription)
        db.session.commit()

    @staticmethod
    def get_by_patient(patient_id):
        return Prescription.query.filter_by(
            patient_id=patient_id
        ).all()

    @staticmethod
    def get_by_doctor(doctor_id):
        return Prescription.query.filter_by(
            doctor_id=doctor_id
        ).all()