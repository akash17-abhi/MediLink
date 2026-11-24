from flask import Blueprint, request

from app.schemas.prescription_schema import (
    validate_prescription,
    prescription_to_dict
)

from app.services.prescription_service import (
    PrescriptionService
)


prescription_bp = Blueprint(
    "prescription",
    __name__,
    url_prefix="/api/prescriptions"
)


# =========================================================
# CREATE PRESCRIPTION
# =========================================================

@prescription_bp.post("/")
def create_prescription():

    data = request.get_json(silent=True) or {}

    if not data:
        return {
            "success": False,
            "message": "Request body is required"
        }, 400

    valid, message = validate_prescription(data)

    if not valid:
        return {
            "success": False,
            "message": message
        }, 400

    prescription, error = PrescriptionService.create(
        data
    )

    if error:
        return {
            "success": False,
            "message": error
        }, 404

    return {
        "success": True,
        "message": "Prescription created successfully",
        "prescription": prescription_to_dict(
            prescription
        )
    }, 201


# =========================================================
# GET ALL PRESCRIPTIONS
# =========================================================

@prescription_bp.get("/")
def get_all():

    prescriptions = PrescriptionService.get_all()

    return {
        "success": True,
        "count": len(prescriptions),
        "prescriptions": [
            prescription_to_dict(p)
            for p in prescriptions
        ]
    }


# =========================================================
# GET PRESCRIPTION BY ID
# =========================================================

@prescription_bp.get("/<int:prescription_id>")
def get_one(prescription_id):

    prescription = PrescriptionService.get_by_id(
        prescription_id
    )

    if not prescription:
        return {
            "success": False,
            "message": "Prescription not found"
        }, 404

    return {
        "success": True,
        "prescription": prescription_to_dict(
            prescription
        )
    }


# =========================================================
# UPDATE PRESCRIPTION
# =========================================================

@prescription_bp.put("/<int:prescription_id>")
def update_prescription(prescription_id):

    data = request.get_json(silent=True) or {}

    if not data:
        return {
            "success": False,
            "message": "Request body is required"
        }, 400

    prescription, error = PrescriptionService.update(
        prescription_id,
        data
    )

    if error:
        return {
            "success": False,
            "message": error
        }, 404

    return {
        "success": True,
        "message": "Prescription updated successfully",
        "prescription": prescription_to_dict(
            prescription
        )
    }


# =========================================================
# DELETE PRESCRIPTION
# =========================================================

@prescription_bp.delete("/<int:prescription_id>")
def delete_prescription(prescription_id):

    deleted = PrescriptionService.delete(
        prescription_id
    )

    if not deleted:
        return {
            "success": False,
            "message": "Prescription not found"
        }, 404

    return {
        "success": True,
        "message": "Prescription deleted successfully"
    }


# =========================================================
# GET PRESCRIPTIONS BY PATIENT
# =========================================================

@prescription_bp.get("/patient/<int:patient_id>")
def get_by_patient(patient_id):

    prescriptions = PrescriptionService.get_by_patient(
        patient_id
    )

    return {
        "success": True,
        "count": len(prescriptions),
        "prescriptions": [
            prescription_to_dict(p)
            for p in prescriptions
        ]
    }


# =========================================================
# GET PRESCRIPTIONS BY DOCTOR
# =========================================================

@prescription_bp.get("/doctor/<int:doctor_id>")
def get_by_doctor(doctor_id):

    prescriptions = PrescriptionService.get_by_doctor(
        doctor_id
    )

    return {
        "success": True,
        "count": len(prescriptions),
        "prescriptions": [
            prescription_to_dict(p)
            for p in prescriptions
        ]
    }