from app.models.payment import Payment
from app.repositories.base_repository import BaseRepository


class PaymentRepository(BaseRepository):
    """Repository for Payment operations"""

    def __init__(self):
        super().__init__(Payment)

    def get_by_bill(self, bill_id):
        return Payment.query.filter_by(
            bill_id=bill_id
        ).all()