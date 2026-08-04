from app.extensions import db
from app.models.hospital import Hospital


class HospitalRepository:

    @staticmethod
    def create(data):
        hospital = Hospital(**data)
        db.session.add(hospital)
        db.session.commit()
        return hospital

    @staticmethod
    def get_all():
        return Hospital.query.all()

    @staticmethod
    def get_by_id(hospital_id):
        return Hospital.query.get(hospital_id)

    @staticmethod
    def update(hospital, data):
        for key, value in data.items():
            setattr(hospital, key, value)

        db.session.commit()
        return hospital

    @staticmethod
    def delete(hospital):
        db.session.delete(hospital)
        db.session.commit()

    @staticmethod
    def get_by_email(email):
        return Hospital.query.filter_by(email=email).first()

    @staticmethod
    def get_by_registration_number(registration_number):
        return Hospital.query.filter_by(
            registration_number=registration_number
        ).first()