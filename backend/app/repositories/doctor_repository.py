from app.extensions import db
from app.models.doctor import Doctor


class DoctorRepository:

    @staticmethod
    def create(doctor):
        db.session.add(doctor)
        db.session.commit()
        return doctor

    @staticmethod
    def get_all():
        return Doctor.query.all()

    @staticmethod
    def get_by_id(doctor_id):
        return Doctor.query.get(doctor_id)

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(doctor):
        db.session.delete(doctor)
        db.session.commit()

    @staticmethod
    def get_by_email(email):
        return Doctor.query.filter_by(email=email).first()