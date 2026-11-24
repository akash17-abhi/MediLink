from app.extensions import db
from app.models.appointment import Appointment


class AppointmentRepository:

    # =========================================================
    # CREATE APPOINTMENT
    # =========================================================

    @staticmethod
    def create(appointment):

        db.session.add(appointment)
        db.session.commit()

        return appointment

    # =========================================================
    # GET ALL APPOINTMENTS
    # =========================================================

    @staticmethod
    def get_all():

        return Appointment.query.all()

    # =========================================================
    # GET APPOINTMENT BY ID
    # =========================================================

    @staticmethod
    def get_by_id(appointment_id):

        return db.session.get(
            Appointment,
            appointment_id
        )

    # =========================================================
    # UPDATE APPOINTMENT
    # =========================================================

    @staticmethod
    def update(appointment, update_data):

        for field, value in update_data.items():

            setattr(
                appointment,
                field,
                value
            )

        db.session.commit()

        return appointment

    # =========================================================
    # DELETE APPOINTMENT
    # =========================================================

    @staticmethod
    def delete(appointment):

        db.session.delete(appointment)
        db.session.commit()

        return True