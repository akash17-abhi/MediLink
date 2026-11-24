from app.extensions import db
from app.models.emergency import Emergency


class EmergencyRepository:
    """Database operations for Emergency."""

    @staticmethod
    def create(emergency):
        db.session.add(emergency)
        db.session.commit()
        db.session.refresh(emergency)
        return emergency

    @staticmethod
    def get_by_id(emergency_id):
        return Emergency.query.get(emergency_id)

    @staticmethod
    def get_all():
        return Emergency.query.order_by(
            Emergency.created_at.desc()
        ).all()

    @staticmethod
    def get_by_patient(patient_id):
        return Emergency.query.filter_by(
            patient_id=patient_id
        ).order_by(
            Emergency.created_at.desc()
        ).all()

    @staticmethod
    def get_by_hospital(hospital_id):
        return Emergency.query.filter_by(
            hospital_id=hospital_id
        ).order_by(
            Emergency.created_at.desc()
        ).all()

    @staticmethod
    def get_active():
        return Emergency.query.filter(
            Emergency.status.in_([
                "Requested",
                "Assigned",
                "Dispatched",
                "On The Way",
                "Arrived",
                "Patient Picked Up",
                "Hospital Arrived"
            ])
        ).order_by(
            Emergency.created_at.desc()
        ).all()

    @staticmethod
    def get_pending():
        return Emergency.query.filter_by(
            status="Requested"
        ).order_by(
            Emergency.created_at.asc()
        ).all()

    @staticmethod
    def update(emergency):
        db.session.commit()
        db.session.refresh(emergency)
        return emergency

    @staticmethod
    def delete(emergency):
        db.session.delete(emergency)
        db.session.commit()