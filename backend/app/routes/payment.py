from flask import Blueprint, request

from app.services.payment_service import PaymentService

from app.schemas.payment_schema import (
    validate_payment,
    payment_to_dict
)

payment_bp = Blueprint(
    "payment",
    __name__,
    url_prefix="/api/payments"
)


@payment_bp.post("/")
def create_payment():

    data = request.get_json()

    valid, message = validate_payment(data)

    if not valid:
        return {
            "success": False,
            "message": message
        }, 400

    payment, error = PaymentService.create(data)

    if error:
        return {
            "success": False,
            "message": error
        }, 404

    return {
        "success": True,
        "message": "Payment completed successfully",
        "payment": payment_to_dict(payment)
    }, 201


@payment_bp.get("/")
def get_all():

    payments = PaymentService.get_all()

    return {
        "success": True,
        "count": len(payments),
        "payments": [
            payment_to_dict(p)
            for p in payments
        ]
    }


@payment_bp.get("/<int:payment_id>")
def get_one(payment_id):

    payment = PaymentService.get_by_id(payment_id)

    if not payment:
        return {
            "success": False,
            "message": "Payment not found"
        }, 404

    return {
        "success": True,
        "payment": payment_to_dict(payment)
    }


@payment_bp.put("/<int:payment_id>")
def update_payment(payment_id):

    payment = PaymentService.update(
        payment_id,
        request.get_json()
    )

    if not payment:
        return {
            "success": False,
            "message": "Payment not found"
        }, 404

    return {
        "success": True,
        "message": "Payment updated successfully",
        "payment": payment_to_dict(payment)
    }


@payment_bp.delete("/<int:payment_id>")
def delete_payment(payment_id):

    deleted = PaymentService.delete(payment_id)

    if not deleted:
        return {
            "success": False,
            "message": "Payment not found"
        }, 404

    return {
        "success": True,
        "message": "Payment deleted successfully"
    }


@payment_bp.get("/bill/<int:bill_id>")
def bill_payments(bill_id):

    payments = PaymentService.get_bill_payments(bill_id)

    return {
        "success": True,
        "count": len(payments),
        "payments": [
            payment_to_dict(p)
            for p in payments
        ]
    }