from flask import Blueprint, request

from app.services.bill_service import BillService

from app.schemas.bill_schema import (
    validate_bill,
    bill_to_dict
)


# =========================================================
# BLUEPRINT
# =========================================================

bill_bp = Blueprint(
    "bill",
    __name__,
    url_prefix="/api/bills"
)


# =========================================================
# CREATE BILL
# =========================================================

@bill_bp.post("/")
def create_bill():

    data = request.get_json(
        silent=True
    ) or {}

    valid, message = validate_bill(
        data
    )

    if not valid:

        return {
            "success": False,
            "message": message
        }, 400

    bill, error = BillService.create(
        data
    )

    if error:

        return {
            "success": False,
            "message": error
        }, 400

    return {
        "success": True,
        "message": "Bill created successfully",
        "bill": bill_to_dict(
            bill
        )
    }, 201


# =========================================================
# GET ALL BILLS
# =========================================================

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
    }, 200


# =========================================================
# GET BILL BY ID
# =========================================================

@bill_bp.get("/<int:bill_id>")
def get_one(bill_id):

    bill = BillService.get_by_id(
        bill_id
    )

    if not bill:

        return {
            "success": False,
            "message": "Bill not found"
        }, 404

    return {
        "success": True,
        "bill": bill_to_dict(
            bill
        )
    }, 200


# =========================================================
# UPDATE BILL
# =========================================================

@bill_bp.put("/<int:bill_id>")
def update_bill(bill_id):

    data = request.get_json(
        silent=True
    ) or {}

    if not data:

        return {
            "success": False,
            "message": "Request body is required"
        }, 400

    bill, error = BillService.update(
        bill_id,
        data
    )

    if error:

        if error == "Bill not found":

            return {
                "success": False,
                "message": error
            }, 404

        return {
            "success": False,
            "message": error
        }, 400

    return {
        "success": True,
        "message": "Bill updated successfully",
        "bill": bill_to_dict(
            bill
        )
    }, 200


# =========================================================
# DELETE BILL
# =========================================================

@bill_bp.delete("/<int:bill_id>")
def delete_bill(bill_id):

    deleted = BillService.delete(
        bill_id
    )

    if not deleted:

        return {
            "success": False,
            "message": "Bill not found"
        }, 404

    return {
        "success": True,
        "message": "Bill deleted successfully"
    }, 200


# =========================================================
# GET PATIENT BILLS
# =========================================================

@bill_bp.get("/patient/<int:patient_id>")
def get_patient_bills(patient_id):

    bills = BillService.get_by_patient(
        patient_id
    )

    return {
        "success": True,
        "count": len(bills),
        "bills": [
            bill_to_dict(b)
            for b in bills
        ]
    }, 200