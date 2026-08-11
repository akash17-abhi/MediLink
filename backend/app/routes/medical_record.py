from flask import Blueprint, request

from app.schemas.medical_record_schema import (
    validate_medical_record,
    medical_record_to_dict
)

from app.services.medical_record_service import (
    MedicalRecordService
)


medical_record_bp = Blueprint(
    "medical_record",
    __name__,
    url_prefix="/api/medical-records"
)


# =========================================================
# CREATE MEDICAL RECORD
# =========================================================

@medical_record_bp.post("/")
def create_record():

    data = request.get_json()

    valid, message = validate_medical_record(data)

    if not valid:
        return {
            "success": False,
            "message": message
        }, 400

    record, error = MedicalRecordService.create(data)

    if error:
        return {
            "success": False,
            "message": error
        }, 404

    return {
        "success": True,
        "message": "Medical record created successfully",
        "medical_record": medical_record_to_dict(record)
    }, 201


# =========================================================
# GET ALL MEDICAL RECORDS
# =========================================================

@medical_record_bp.get("/")
def get_all():

    records = MedicalRecordService.get_all()

    return {
        "success": True,
        "count": len(records),
        "medical_records": [
            medical_record_to_dict(record)
            for record in records
        ]
    }


# =========================================================
# GET MEDICAL RECORD BY ID
# =========================================================

@medical_record_bp.get("/<int:record_id>")
def get_one(record_id):

    record = MedicalRecordService.get_by_id(record_id)

    if not record:
        return {
            "success": False,
            "message": "Medical record not found"
        }, 404

    return {
        "success": True,
        "medical_record": medical_record_to_dict(record)
    }


# =========================================================
# UPDATE MEDICAL RECORD
# =========================================================

@medical_record_bp.put("/<int:record_id>")
def update_record(record_id):

    data = request.get_json()

    record = MedicalRecordService.update(
        record_id,
        data
    )

    if not record:
        return {
            "success": False,
            "message": "Medical record not found"
        }, 404

    return {
        "success": True,
        "message": "Medical record updated successfully",
        "medical_record": medical_record_to_dict(record)
    }


# =========================================================
# DELETE MEDICAL RECORD
# =========================================================

@medical_record_bp.delete("/<int:record_id>")
def delete_record(record_id):

    deleted = MedicalRecordService.delete(record_id)

    if not deleted:
        return {
            "success": False,
            "message": "Medical record not found"
        }, 404

    return {
        "success": True,
        "message": "Medical record deleted successfully"
    }


# =========================================================
# GET RECORDS BY PATIENT
# =========================================================

@medical_record_bp.get("/patient/<int:patient_id>")
def get_patient_records(patient_id):

    records = MedicalRecordService.get_by_patient(
        patient_id
    )

    return {
        "success": True,
        "count": len(records),
        "medical_records": [
            medical_record_to_dict(record)
            for record in records
        ]
    }


# =========================================================
# GET RECORDS BY DOCTOR
# =========================================================

@medical_record_bp.get("/doctor/<int:doctor_id>")
def get_doctor_records(doctor_id):

    records = MedicalRecordService.get_by_doctor(
        doctor_id
    )

    return {
        "success": True,
        "count": len(records),
        "medical_records": [
            medical_record_to_dict(record)
            for record in records
        ]
    }