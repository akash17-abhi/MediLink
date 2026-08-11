from flask import Blueprint, request

from app.schemas.appointment_schema import (
    validate_appointment,
    appointment_to_dict
)

from app.services.appointment_service import (
    AppointmentService
)


appointment_bp = Blueprint(
    "appointment",
    __name__,
    url_prefix="/api/appointments"
)


# =========================================================
# CREATE APPOINTMENT
# =========================================================

@appointment_bp.post("/")
def create_appointment():

    data = request.get_json()

    valid, message = validate_appointment(
        data
    )

    if not valid:

        return {
            "success": False,
            "message": message
        }, 400

    appointment, error = AppointmentService.create(
        data
    )

    if error:

        return {
            "success": False,
            "message": error
        }, 400

    return {
        "success": True,
        "message": "Appointment created successfully",
        "appointment": appointment_to_dict(
            appointment
        )
    }, 201


# =========================================================
# GET ALL APPOINTMENTS
# =========================================================

@appointment_bp.get("/")
def get_all():

    appointments = AppointmentService.get_all()

    return {
        "success": True,
        "count": len(appointments),
        "appointments": [
            appointment_to_dict(appointment)
            for appointment in appointments
        ]
    }


# =========================================================
# GET APPOINTMENT BY ID
# =========================================================

@appointment_bp.get("/<int:appointment_id>")
def get_one(appointment_id):

    appointment = AppointmentService.get_by_id(
        appointment_id
    )

    if not appointment:

        return {
            "success": False,
            "message": "Appointment not found"
        }, 404

    return {
        "success": True,
        "appointment": appointment_to_dict(
            appointment
        )
    }


# =========================================================
# UPDATE APPOINTMENT
# =========================================================

@appointment_bp.put("/<int:appointment_id>")
def update_appointment(appointment_id):

    data = request.get_json()

    if not data:

        return {
            "success": False,
            "message": "Request body is required"
        }, 400

    appointment, error = AppointmentService.update(
        appointment_id,
        data
    )

    if error:

        if error == "Appointment not found":

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
        "message": "Appointment updated successfully",
        "appointment": appointment_to_dict(
            appointment
        )
    }


# =========================================================
# DELETE APPOINTMENT
# =========================================================

@appointment_bp.delete("/<int:appointment_id>")
def delete_appointment(appointment_id):

    deleted = AppointmentService.delete(
        appointment_id
    )

    if not deleted:

        return {
            "success": False,
            "message": "Appointment not found"
        }, 404

    return {
        "success": True,
        "message": "Appointment deleted successfully"
    }