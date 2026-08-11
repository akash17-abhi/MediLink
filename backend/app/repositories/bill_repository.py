from app.extensions import db
from app.models.bill import Bill


class BillRepository:

    @staticmethod
    def create(bill):
        db.session.add(bill)
        db.session.commit()
        return bill

    @staticmethod
    def get_all():
        return Bill.query.all()

    @staticmethod
    def get_by_id(bill_id):
        return Bill.query.get(bill_id)

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(bill):
        db.session.delete(bill)
        db.session.commit()

    @staticmethod
    def get_by_patient(patient_id):
        return Bill.query.filter_by(
            patient_id=patient_id
        ).all()