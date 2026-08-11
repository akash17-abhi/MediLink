from app.extensions import db
from app.models.laboratory import Laboratory


class LaboratoryRepository:

    @staticmethod
    def create(test):
        db.session.add(test)
        db.session.commit()
        return test

    @staticmethod
    def get_all():
        return Laboratory.query.all()

    @staticmethod
    def get_by_id(test_id):
        return Laboratory.query.get(test_id)

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(test):
        db.session.delete(test)
        db.session.commit()

    @staticmethod
    def get_by_patient(patient_id):
        return Laboratory.query.filter_by(
            patient_id=patient_id
        ).all()

    @staticmethod
    def get_by_doctor(doctor_id):
        return Laboratory.query.filter_by(
            doctor_id=doctor_id
        ).all()