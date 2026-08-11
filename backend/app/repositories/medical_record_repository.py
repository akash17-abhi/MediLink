from app.extensions import db
from app.models.medical_record import MedicalRecord


class MedicalRecordRepository:

    @staticmethod
    def create(record):
        db.session.add(record)
        db.session.commit()
        return record

    @staticmethod
    def get_all():
        return MedicalRecord.query.all()

    @staticmethod
    def get_by_id(record_id):
        return MedicalRecord.query.get(record_id)

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(record):
        db.session.delete(record)
        db.session.commit()

    @staticmethod
    def get_by_patient(patient_id):
        return MedicalRecord.query.filter_by(
            patient_id=patient_id
        ).all()

    @staticmethod
    def get_by_doctor(doctor_id):
        return MedicalRecord.query.filter_by(
            doctor_id=doctor_id
        ).all()