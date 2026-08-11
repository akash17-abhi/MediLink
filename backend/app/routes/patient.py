from flask import Blueprint, request

from app.schemas.patient_schema import (
    validate_patient,
    patient_to_dict
)

from app.services.patient_service import PatientService


# =========================================================
# PATIENT BLUEPRINT
# =========================================================

patient_bp = Blueprint(
    "patient",
    __name__,
    url_prefix="/api/patients"
)


# =========================================================
# CREATE PATIENT
# =========================================================

@patient_bp.post("/")
def create_patient():

    # -----------------------------------------------------
    # Check JSON request
    # -----------------------------------------------------

    if not request.is_json:
        return {
            "success": False,
            "message": "Request Content-Type must be application/json"
        }, 415

    data = request.get_json(silent=True)

    if data is None:
        return {
            "success": False,
            "message": "Invalid JSON request body"
        }, 400

    # -----------------------------------------------------
    # Validate patient data
    # -----------------------------------------------------

    valid, message = validate_patient(data)

    if not valid:
        return {
            "success": False,
            "message": message
        }, 400

    # -----------------------------------------------------
    # Create patient
    # -----------------------------------------------------

    patient, error = PatientService.create(data)

    if error:
        return {
            "success": False,
            "message": error
        }, 409

    # -----------------------------------------------------
    # Response
    # -----------------------------------------------------

    return {
        "success": True,
        "message": "Patient created successfully",
        "patient": patient_to_dict(patient)
    }, 201


# =========================================================
# GET ALL PATIENTS
# =========================================================

@patient_bp.get("/")
def get_all_patients():

    patients = PatientService.get_all()

    return {
        "success": True,
        "count": len(patients),
        "patients": [
            patient_to_dict(patient)
            for patient in patients
        ]
    }, 200


# =========================================================
# GET PATIENT BY ID
# =========================================================

@patient_bp.get("/<int:patient_id>")
def get_patient(patient_id):

    patient = PatientService.get_by_id(
        patient_id
    )

    if not patient:

        return {
            "success": False,
            "message": "Patient not found"
        }, 404

    return {
        "success": True,
        "patient": patient_to_dict(patient)
    }, 200


# =========================================================
# UPDATE PATIENT
# =========================================================

@patient_bp.put("/<int:patient_id>")
def update_patient(patient_id):

    # -----------------------------------------------------
    # Check JSON request
    # -----------------------------------------------------

    if not request.is_json:

        return {
            "success": False,
            "message": "Request Content-Type must be application/json"
        }, 415

    data = request.get_json(silent=True)

    if data is None:

        return {
            "success": False,
            "message": "Invalid JSON request body"
        }, 400

    # -----------------------------------------------------
    # Check whether patient exists
    # -----------------------------------------------------

    existing_patient = PatientService.get_by_id(
        patient_id
    )

    if not existing_patient:

        return {
            "success": False,
            "message": "Patient not found"
        }, 404

    # -----------------------------------------------------
    # Prevent changing protected fields
    # -----------------------------------------------------

    protected_fields = [
        "id",
        "created_at",
        "updated_at"
    ]

    for field in protected_fields:
        data.pop(field, None)

    # -----------------------------------------------------
    # Update patient
    # -----------------------------------------------------

    patient = PatientService.update(
        patient_id,
        data
    )

    if not patient:

        return {
            "success": False,
            "message": "Patient not found"
        }, 404

    return {
        "success": True,
        "message": "Patient updated successfully",
        "patient": patient_to_dict(patient)
    }, 200


# =========================================================
# DELETE PATIENT
# =========================================================

@patient_bp.delete("/<int:patient_id>")
def delete_patient(patient_id):

    deleted = PatientService.delete(
        patient_id
    )

    if not deleted:

        return {
            "success": False,
            "message": "Patient not found"
        }, 404

    return {
        "success": True,
        "message": "Patient deleted successfully"
    }, 200