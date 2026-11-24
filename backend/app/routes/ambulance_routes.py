from flask import Blueprint, request

from app.schemas.ambulance_schema import (
    validate_ambulance,
    ambulance_to_dict
)

from app.services.ambulance_service import (
    AmbulanceService
)


ambulance_bp = Blueprint(
    "ambulance",
    __name__,
    url_prefix="/api/ambulances"
)


# =========================================================
# CREATE AMBULANCE
# =========================================================

@ambulance_bp.post("/")
def create_ambulance():

    data = request.get_json(silent=True) or {}

    if not data:

        return {
            "success": False,
            "message": "Request body is required"
        }, 400

    valid, message = validate_ambulance(data)

    if not valid:

        return {
            "success": False,
            "message": message
        }, 400

    ambulance, error = AmbulanceService.create(
        data
    )

    if error:

        status_code = 404

        if (
            "already exists"
            in error.lower()
        ):

            status_code = 409

        return {
            "success": False,
            "message": error
        }, status_code

    return {
        "success": True,
        "message": "Ambulance created successfully",
        "ambulance": ambulance_to_dict(
            ambulance
        )
    }, 201


# =========================================================
# GET ALL AMBULANCES
# =========================================================

@ambulance_bp.get("/")
def get_all():

    ambulances = AmbulanceService.get_all()

    return {
        "success": True,
        "count": len(ambulances),
        "ambulances": [
            ambulance_to_dict(a)
            for a in ambulances
        ]
    }


# =========================================================
# GET AMBULANCE BY ID
# =========================================================

@ambulance_bp.get("/<int:ambulance_id>")
def get_one(ambulance_id):

    ambulance = AmbulanceService.get_by_id(
        ambulance_id
    )

    if not ambulance:

        return {
            "success": False,
            "message": "Ambulance not found"
        }, 404

    return {
        "success": True,
        "ambulance": ambulance_to_dict(
            ambulance
        )
    }


# =========================================================
# UPDATE AMBULANCE
# =========================================================

@ambulance_bp.put("/<int:ambulance_id>")
def update_ambulance(ambulance_id):

    data = request.get_json(silent=True) or {}

    if not data:

        return {
            "success": False,
            "message": "Request body is required"
        }, 400

    ambulance, error = AmbulanceService.update(
        ambulance_id,
        data
    )

    if error:

        status_code = 404

        if (
            "already exists"
            in error.lower()
        ):

            status_code = 409

        return {
            "success": False,
            "message": error
        }, status_code

    return {
        "success": True,
        "message": "Ambulance updated successfully",
        "ambulance": ambulance_to_dict(
            ambulance
        )
    }


# =========================================================
# DELETE AMBULANCE
# =========================================================

@ambulance_bp.delete("/<int:ambulance_id>")
def delete_ambulance(ambulance_id):

    deleted = AmbulanceService.delete(
        ambulance_id
    )

    if not deleted:

        return {
            "success": False,
            "message": "Ambulance not found"
        }, 404

    return {
        "success": True,
        "message": "Ambulance deleted successfully"
    }


# =========================================================
# GET AMBULANCES BY HOSPITAL
# =========================================================

@ambulance_bp.get("/hospital/<int:hospital_id>")
def get_by_hospital(hospital_id):

    ambulances = AmbulanceService.get_by_hospital(
        hospital_id
    )

    return {
        "success": True,
        "count": len(ambulances),
        "ambulances": [
            ambulance_to_dict(a)
            for a in ambulances
        ]
    }


# =========================================================
# GET AVAILABLE AMBULANCES
# =========================================================

@ambulance_bp.get("/available")
def get_available():

    ambulances = AmbulanceService.get_available()

    return {
        "success": True,
        "count": len(ambulances),
        "ambulances": [
            ambulance_to_dict(a)
            for a in ambulances
        ]
    }


# =========================================================
# GET AVAILABLE AMBULANCES BY HOSPITAL
# =========================================================

@ambulance_bp.get(
    "/available/hospital/<int:hospital_id>"
)
def get_available_by_hospital(hospital_id):

    ambulances = (
        AmbulanceService
        .get_available_by_hospital(
            hospital_id
        )
    )

    return {
        "success": True,
        "count": len(ambulances),
        "ambulances": [
            ambulance_to_dict(a)
            for a in ambulances
        ]
    }


# =========================================================
# GET EMERGENCY AVAILABLE AMBULANCES
# =========================================================

@ambulance_bp.get("/emergency/available")
def get_emergency_available():

    ambulances = (
        AmbulanceService
        .get_emergency_available()
    )

    return {
        "success": True,
        "count": len(ambulances),
        "ambulances": [
            ambulance_to_dict(a)
            for a in ambulances
        ]
    }