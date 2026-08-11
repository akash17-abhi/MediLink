from flask import Blueprint, request

from app.services.bill_service import BillService

from app.schemas.bill_schema import (
    validate_bill,
    bill_to_dict
)

bill_bp = Blueprint(
    "bill",
    __name__,
    url_prefix="/api/bills"
)


@bill_bp.post("/")
def create_bill():

    data = request.get_json()

    valid, message = validate_bill(data)

    if not valid:
        return {
            "success": False,
            "message": message
        }, 400

    bill, error = BillService.create(data)

    if error:
        return {
            "success": False,
            "message": error
        }, 404

    return {
        "success": True,
        "message": "Bill created successfully",
        "bill": bill_to_dict(bill)
    }, 201


@bill_bp.get("/")
def get_all():

    bills = BillService.get_all()

    return {
        "success": True,
        "count": len(bills),
        "bills": [
            bill_to_dict(b)
            for b in bills
        ]
    }


@bill_bp.get("/<int:bill_id>")
def get_one(bill_id):

    bill = BillService.get_by_id(bill_id)

    if not bill:
        return {
            "success": False,
            "message": "Bill not found"
        }, 404

    return {
        "success": True,
        "bill": bill_to_dict(bill)
    }


@bill_bp.put("/<int:bill_id>")
def update_bill(bill_id):

    bill = BillService.update(
        bill_id,
        request.get_json()
    )

    if not bill:
        return {
            "success": False,
            "message": "Bill not found"
        }, 404

    return {
        "success": True,
        "message": "Bill updated successfully",
        "bill": bill_to_dict(bill)
    }


@bill_bp.delete("/<int:bill_id>")
def delete_bill(bill_id):

    deleted = BillService.delete(bill_id)

    if not deleted:
        return {
            "success": False,
            "message": "Bill not found"
        }, 404

    return {
        "success": True,
        "message": "Bill deleted successfully"
    }


@bill_bp.get("/patient/<int:patient_id>")
def get_patient_bills(patient_id):

    bills = BillService.get_by_patient(patient_id)

    return {
        "success": True,
        "count": len(bills),
        "bills": [
            bill_to_dict(b)
            for b in bills
        ]
    }