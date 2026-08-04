from flask import Blueprint, request

from app.schemas.doctor_schema import (
    validate_doctor,
    doctor_to_dict
)
from app.services.doctor_service import DoctorService

doctor_bp = Blueprint(
    "doctor",
    __name__,
    url_prefix="/api/doctors"
)


@doctor_bp.post("/")
def create_doctor():

    data = request.get_json()

    valid, message = validate_doctor(data)

    if not valid:
        return {
            "success": False,
            "message": message
        }, 400

    doctor, error = DoctorService.create(data)

    if error:
        return {
            "success": False,
            "message": error
        }, 409

    return {
        "success": True,
        "message": "Doctor created successfully",
        "doctor": doctor_to_dict(doctor)
    }, 201


@doctor_bp.get("/")
def get_all():

    doctors = DoctorService.get_all()

    return {
        "success": True,
        "count": len(doctors),
        "doctors": [
            doctor_to_dict(d)
            for d in doctors
        ]
    }


@doctor_bp.get("/<int:doctor_id>")
def get_one(doctor_id):

    doctor = DoctorService.get_by_id(doctor_id)

    if not doctor:
        return {
            "success": False,
            "message": "Doctor not found"
        }, 404

    return {
        "success": True,
        "doctor": doctor_to_dict(doctor)
    }


@doctor_bp.put("/<int:doctor_id>")
def update_doctor(doctor_id):

    data = request.get_json()

    doctor = DoctorService.update(
        doctor_id,
        data
    )

    if not doctor:
        return {
            "success": False,
            "message": "Doctor not found"
        }, 404

    return {
        "success": True,
        "message": "Doctor updated successfully",
        "doctor": doctor_to_dict(doctor)
    }


@doctor_bp.delete("/<int:doctor_id>")
def delete_doctor(doctor_id):

    deleted = DoctorService.delete(doctor_id)

    if not deleted:
        return {
            "success": False,
            "message": "Doctor not found"
        }, 404

    return {
        "success": True,
        "message": "Doctor deleted successfully"
    }