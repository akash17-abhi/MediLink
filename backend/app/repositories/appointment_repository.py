from app.extensions import db
from app.models.appointment import Appointment


class AppointmentRepository:

    @staticmethod
    def create(appointment):
        db.session.add(appointment)
        db.session.commit()
        return appointment

    @staticmethod
    def get_all():
        return Appointment.query.all()

    @staticmethod
    def get_by_id(appointment_id):
        return Appointment.query.get(appointment_id)

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(appointment):
        db.session.delete(appointment)
        db.session.commit()