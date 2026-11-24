from flask import Blueprint, request

from app.schemas.doctor_schedule_schema import (
    schedule_to_dict
)

from app.services.doctor_schedule_service import (
    DoctorScheduleService
)

from app.validators.doctor_schedule_validator import (
    validate_doctor_schedule
)


# =========================================================
# BLUEPRINT
# =========================================================

schedule_bp = Blueprint(
    "doctor_schedule",
    __name__,
    url_prefix="/api/schedules"
)


# =========================================================
# CREATE SCHEDULE
# =========================================================

@schedule_bp.post("/")
def create_schedule():

    data = request.get_json(silent=True)

    valid, message = validate_doctor_schedule(
        data
    )

    if not valid:

        return {
            "success": False,
            "message": message
        }, 400

    schedule, error = DoctorScheduleService.create(
        data
    )

    if error:

        return {
            "success": False,
            "message": error
        }, 404

    return {
        "success": True,
        "message": "Schedule created successfully",
        "schedule": schedule_to_dict(schedule)
    }, 201


# =========================================================
# GET ALL SCHEDULES
# =========================================================

@schedule_bp.get("/")
def get_all():

    schedules = DoctorScheduleService.get_all()

    return {
        "success": True,
        "count": len(schedules),
        "schedules": [
            schedule_to_dict(schedule)
            for schedule in schedules
        ]
    }, 200


# =========================================================
# GET SCHEDULES BY DOCTOR
# =========================================================

@schedule_bp.get("/doctor/<int:doctor_id>")
def get_by_doctor(doctor_id):

    schedules = DoctorScheduleService.get_by_doctor(
        doctor_id
    )

    return {
        "success": True,
        "count": len(schedules),
        "schedules": [
            schedule_to_dict(schedule)
            for schedule in schedules
        ]
    }, 200


# =========================================================
# GET SINGLE SCHEDULE
# =========================================================

@schedule_bp.get("/<int:schedule_id>")
def get_one(schedule_id):

    schedule = DoctorScheduleService.get_by_id(
        schedule_id
    )

    if not schedule:

        return {
            "success": False,
            "message": "Schedule not found"
        }, 404

    return {
        "success": True,
        "schedule": schedule_to_dict(schedule)
    }, 200


# =========================================================
# UPDATE SCHEDULE
# =========================================================

@schedule_bp.put("/<int:schedule_id>")
def update_schedule(schedule_id):

    data = request.get_json(silent=True)

    if not data:

        return {
            "success": False,
            "message": "Request body is required"
        }, 400

    schedule, error = DoctorScheduleService.update(
        schedule_id,
        data
    )

    if error:

        if error == "Schedule not found":

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
        "message": "Schedule updated successfully",
        "schedule": schedule_to_dict(schedule)
    }, 200
# =========================================================
# DELETE SCHEDULE
# =========================================================

@schedule_bp.delete("/<int:schedule_id>")
def delete_schedule(schedule_id):

    deleted = DoctorScheduleService.delete(
        schedule_id
    )

    if not deleted:

        return {
            "success": False,
            "message": "Schedule not found"
        }, 404

    return {
        "success": True,
        "message": "Schedule deleted successfully"
    }, 200