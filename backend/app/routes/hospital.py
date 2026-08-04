from flask import Blueprint, request

from app.schemas.hospital_schema import hospital_to_dict
from app.services.hospital_service import HospitalService
from app.validators.hospital_validator import validate_hospital

hospital_bp = Blueprint(
    "hospital",
    __name__,
    url_prefix="/api/hospitals"
)


@hospital_bp.post("/")
def create_hospital():

    data = request.get_json()

    valid, message = validate_hospital(data)

    if not valid:
        return {
            "success": False,
            "message": message
        }, 400

    hospital, error = HospitalService.create_hospital(data)

    if error:
        return {
            "success": False,
            "message": error
        }, 409

    return {
        "success": True,
        "message": "Hospital created successfully",
        "hospital": hospital_to_dict(hospital)
    }, 201


@hospital_bp.get("/")
def get_all_hospitals():

    hospitals = HospitalService.get_all_hospitals()

    return {
        "success": True,
        "count": len(hospitals),
        "hospitals": [
            hospital_to_dict(h)
            for h in hospitals
        ]
    }


@hospital_bp.get("/<int:hospital_id>")
def get_hospital(hospital_id):

    hospital = HospitalService.get_hospital(hospital_id)

    if not hospital:
        return {
            "success": False,
            "message": "Hospital not found"
        }, 404

    return {
        "success": True,
        "hospital": hospital_to_dict(hospital)
    }


@hospital_bp.put("/<int:hospital_id>")
def update_hospital(hospital_id):

    hospital = HospitalService.get_hospital(hospital_id)

    if not hospital:
        return {
            "success": False,
            "message": "Hospital not found"
        }, 404

    data = request.get_json()

    hospital = HospitalService.update_hospital(
        hospital,
        data
    )

    return {
        "success": True,
        "message": "Hospital updated successfully",
        "hospital": hospital_to_dict(hospital)
    }


@hospital_bp.delete("/<int:hospital_id>")
def delete_hospital(hospital_id):

    hospital = HospitalService.get_hospital(hospital_id)

    if not hospital:
        return {
            "success": False,
            "message": "Hospital not found"
        }, 404

    HospitalService.delete_hospital(hospital)

    return {
        "success": True,
        "message": "Hospital deleted successfully"
    }