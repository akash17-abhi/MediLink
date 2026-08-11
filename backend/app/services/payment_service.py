from datetime import datetime

from app.models.bill import Bill
from app.models.payment import Payment

from app.repositories.payment_repository import PaymentRepository


class PaymentService:

    repo = PaymentRepository()

    @staticmethod
    def create(data):

        bill = Bill.query.get(data["bill_id"])

        if not bill:
            return None, "Bill not found"

        payment = Payment(
            bill_id=data["bill_id"],
            amount=data["amount"],
            payment_method=data["payment_method"],
            transaction_id=data.get("transaction_id"),
            payment_status=data.get(
                "payment_status",
                "Completed"
            ),
            payment_date=datetime.utcnow(),
            remarks=data.get("remarks")
        )

        bill.payment_status = payment.payment_status

        PaymentService.repo.create(payment)

        return payment, None

    @staticmethod
    def get_all():
        return PaymentService.repo.get_all()

    @staticmethod
    def get_by_id(payment_id):
        return PaymentService.repo.get_by_id(payment_id)

    @staticmethod
    def update(payment_id, data):

        payment = PaymentService.repo.get_by_id(payment_id)

        if not payment:
            return None

        for key, value in data.items():
            setattr(payment, key, value)

        PaymentService.repo.update()

        return payment

    @staticmethod
    def delete(payment_id):

        payment = PaymentService.repo.get_by_id(payment_id)

        if not payment:
            return False

        PaymentService.repo.delete(payment)

        return True

    @staticmethod
    def get_bill_payments(bill_id):
        return PaymentService.repo.get_by_bill(bill_id)