from datetime import datetime


def validate_payment(data):

    required_fields = [
        "bill_id",
        "amount",
        "payment_method"
    ]

    for field in required_fields:
        if field not in data or data[field] in (None, ""):
            return False, f"{field} is required"

    return True, ""


def payment_to_dict(payment):

    return {
        "id": payment.id,
        "bill_id": payment.bill_id,
        "amount": payment.amount,
        "payment_method": payment.payment_method,
        "transaction_id": payment.transaction_id,
        "payment_status": payment.payment_status,
        "payment_date": (
            payment.payment_date.strftime("%Y-%m-%d %H:%M:%S")
            if payment.payment_date else None
        ),
        "remarks": payment.remarks,
        "created_at": (
            payment.created_at.strftime("%Y-%m-%d %H:%M:%S")
            if payment.created_at else None
        ),
        "updated_at": (
            payment.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            if payment.updated_at else None
        )
    }