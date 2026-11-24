from flask import Blueprint, request

from app.schemas.hospital_schema import hospital_to_dict
from app.services.hospital_service import HospitalService
from app.validators.hospital_validator import validate_hospital

from app.utils.role_required import role_required


hospital_bp = Blueprint(
    "hospital",
    __name__,
    url_prefix="/api/hospitals"
)


# =========================================================
# CREATE HOSPITAL
# =========================================================

@hospital_bp.post("/")
@role_required("Admin")
def create_hospital():

    data = request.get_json()

    if not data:

        return {
            "success": False,
            "message": "Request body is required."
        }, 400


    valid, message = validate_hospital(
        data
    )

    if not valid:

        return {
            "success": False,
            "message": message
        }, 400


    hospital, error = HospitalService.create_hospital(
        data
    )

    if error:

        return {
            "success": False,
            "message": error
        }, 409


    return {
        "success": True,
        "message": "Hospital created successfully",
        "hospital": hospital_to_dict(
            hospital
        )
    }, 201


# =========================================================
# GET ALL HOSPITALS
# =========================================================

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
    }, 200


# =========================================================
# GET SINGLE HOSPITAL
# =========================================================

@hospital_bp.get("/<int:hospital_id>")
def get_hospital(hospital_id):

    hospital = HospitalService.get_hospital(
        hospital_id
    )

    if not hospital:

        return {
            "success": False,
            "message": "Hospital not found"
        }, 404


    return {
        "success": True,
        "hospital": hospital_to_dict(
            hospital
        )
    }, 200


# =========================================================
# UPDATE HOSPITAL
# =========================================================

@hospital_bp.put("/<int:hospital_id>")
@role_required("Admin")
def update_hospital(hospital_id):

    hospital = HospitalService.get_hospital(
        hospital_id
    )

    if not hospital:

        return {
            "success": False,
            "message": "Hospital not found"
        }, 404


    data = request.get_json()

    if not data:

        return {
            "success": False,
            "message": "Request body is required."
        }, 400


    hospital = HospitalService.update_hospital(
        hospital,
        data
    )


    return {
        "success": True,
        "message": "Hospital updated successfully",
        "hospital": hospital_to_dict(
            hospital
        )
    }, 200


# =========================================================
# DELETE HOSPITAL
# =========================================================

@hospital_bp.delete("/<int:hospital_id>")
@role_required("Admin")
def delete_hospital(hospital_id):

    hospital = HospitalService.get_hospital(
        hospital_id
    )

    if not hospital:

        return {
            "success": False,
            "message": "Hospital not found"
        }, 404


    HospitalService.delete_hospital(
        hospital
    )


    return {
        "success": True,
        "message": "Hospital deleted successfully"
    }, 200


# =========================================================
# ASSIGN HOSPITAL TO USER
# ADMIN ONLY
# =========================================================

@hospital_bp.post(
    "/<int:hospital_id>/assign-user"
)
@role_required("Admin")
def assign_hospital_to_user(hospital_id):

    data = request.get_json()

    if not data:

        return {
            "success": False,
            "message": "Request body is required."
        }, 400


    user_id = data.get("user_id")

    if not user_id:

        return {
            "success": False,
            "message": "user_id is required."
        }, 400


    try:

        user_id = int(user_id)

    except (
        TypeError,
        ValueError
    ):

        return {
            "success": False,
            "message": "user_id must be an integer."
        }, 400


    hospital, error = HospitalService.assign_hospital_to_user(
        hospital_id,
        user_id
    )


    if error:

        status_code = 404 if error in [
            "Hospital not found.",
            "User not found."
        ] else 409

        return {
            "success": False,
            "message": error
        }, status_code


    return {
        "success": True,
        "message": "Hospital assigned to user successfully",
        "hospital": hospital_to_dict(
            hospital
        )
    }, 200


# =========================================================
# UNASSIGN HOSPITAL FROM USER
# ADMIN ONLY
# =========================================================

@hospital_bp.delete(
    "/<int:hospital_id>/assign-user"
)
@role_required("Admin")
def unassign_hospital_from_user(
    hospital_id
):

    hospital, error = HospitalService.unassign_hospital_from_user(
        hospital_id
    )


    if error:

        status_code = (
            404
            if error == "Hospital not found."
            else 409
        )

        return {
            "success": False,
            "message": error
        }, status_code


    return {
        "success": True,
        "message": "Hospital unassigned from user successfully",
        "hospital": hospital_to_dict(
            hospital
        )
    }, 200