from flask import Blueprint, request

from app.schemas.laboratory_schema import (
    validate_laboratory,
    laboratory_to_dict
)

from app.services.laboratory_service import LaboratoryService


laboratory_bp = Blueprint(
    "laboratory",
    __name__,
    url_prefix="/api/laboratories"
)


@laboratory_bp.post("/")
def create_test():

    data = request.get_json()

    valid, message = validate_laboratory(data)

    if not valid:
        return {
            "success": False,
            "message": message
        }, 400

    test, error = LaboratoryService.create(data)

    if error:
        return {
            "success": False,
            "message": error
        }, 404

    return {
        "success": True,
        "message": "Laboratory test created successfully",
        "laboratory": laboratory_to_dict(test)
    }, 201


@laboratory_bp.get("/")
def get_all():

    tests = LaboratoryService.get_all()

    return {
        "success": True,
        "count": len(tests),
        "laboratories": [
            laboratory_to_dict(t)
            for t in tests
        ]
    }


@laboratory_bp.get("/<int:test_id>")
def get_one(test_id):

    test = LaboratoryService.get_by_id(test_id)

    if not test:
        return {
            "success": False,
            "message": "Laboratory test not found"
        }, 404

    return {
        "success": True,
        "laboratory": laboratory_to_dict(test)
    }


@laboratory_bp.put("/<int:test_id>")
def update_test(test_id):

    test = LaboratoryService.update(
        test_id,
        request.get_json()
    )

    if not test:
        return {
            "success": False,
            "message": "Laboratory test not found"
        }, 404

    return {
        "success": True,
        "message": "Laboratory test updated successfully",
        "laboratory": laboratory_to_dict(test)
    }


@laboratory_bp.delete("/<int:test_id>")
def delete_test(test_id):

    deleted = LaboratoryService.delete(test_id)

    if not deleted:
        return {
            "success": False,
            "message": "Laboratory test not found"
        }, 404

    return {
        "success": True,
        "message": "Laboratory test deleted successfully"
    }


@laboratory_bp.get("/patient/<int:patient_id>")
def get_patient_tests(patient_id):

    tests = LaboratoryService.get_by_patient(patient_id)

    return {
        "success": True,
        "count": len(tests),
        "laboratories": [
            laboratory_to_dict(t)
            for t in tests
        ]
    }


@laboratory_bp.get("/doctor/<int:doctor_id>")
def get_doctor_tests(doctor_id):

    tests = LaboratoryService.get_by_doctor(doctor_id)

    return {
        "success": True,
        "count": len(tests),
        "laboratories": [
            laboratory_to_dict(t)
            for t in tests
        ]
    }