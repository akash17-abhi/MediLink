from app.extensions import db
from app.models.doctor_schedule import DoctorSchedule


class DoctorScheduleRepository:

    # =========================================================
    # CREATE
    # =========================================================

    @staticmethod
    def create(schedule):

        db.session.add(schedule)
        db.session.commit()

        return schedule

    # =========================================================
    # GET ALL
    # =========================================================

    @staticmethod
    def get_all():

        return DoctorSchedule.query.all()

    # =========================================================
    # GET BY ID
    # =========================================================

    @staticmethod
    def get_by_id(schedule_id):

        return DoctorSchedule.query.get(schedule_id)

    # =========================================================
    # GET BY DOCTOR
    # =========================================================

    @staticmethod
    def get_by_doctor(doctor_id):

        return DoctorSchedule.query.filter_by(
            doctor_id=doctor_id
        ).all()

    # =========================================================
    # UPDATE
    # =========================================================

    @staticmethod
    def update(schedule, data):

        for key, value in data.items():

            setattr(
                schedule,
                key,
                value
            )

        db.session.commit()

        return schedule

    # =========================================================
    # DELETE
    # =========================================================

    @staticmethod
    def delete(schedule):

        db.session.delete(schedule)
        db.session.commit()

        return True