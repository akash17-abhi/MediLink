from app import db
from app.models.base_model import BaseModel


class Payment(BaseModel):

    __tablename__ = "payments"

    bill_id = db.Column(
        db.Integer,
        db.ForeignKey("bills.id"),
        nullable=False
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    payment_method = db.Column(
        db.String(50),
        nullable=False
    )

    transaction_id = db.Column(
        db.String(150),
        unique=True
    )

    payment_status = db.Column(
        db.String(50),
        default="Pending"
    )

    payment_date = db.Column(
        db.DateTime
    )

    remarks = db.Column(
        db.Text
    )