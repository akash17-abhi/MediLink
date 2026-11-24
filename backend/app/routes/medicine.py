from flask import Blueprint, request

from app.schemas.medicine_schema import (
    validate_medicine,
    medicine_to_dict
)

from app.services.medicine_service import (
    MedicineService
)


medicine_bp = Blueprint(
    "medicine",
    __name__,
    url_prefix="/api/medicines"
)


# =========================================================
# CREATE MEDICINE
# =========================================================

@medicine_bp.post("/")
def create_medicine():

    data = request.get_json(silent=True)

    if not data:
        return {
            "success": False,
            "message": "Request body is required"
        }, 400

    valid, message = validate_medicine(data)

    if not valid:
        return {
            "success": False,
            "message": message
        }, 400

    medicine, error = MedicineService.create(data)

    if error:
        return {
            "success": False,
            "message": error
        }, 409

    return {
        "success": True,
        "message": "Medicine added successfully",
        "medicine": medicine_to_dict(medicine)
    }, 201


# =========================================================
# GET ALL MEDICINES
# =========================================================

@medicine_bp.get("/")
def get_all():

    medicines = MedicineService.get_all()

    return {
        "success": True,
        "count": len(medicines),
        "medicines": [
            medicine_to_dict(m)
            for m in medicines
        ]
    }


# =========================================================
# GET MEDICINE BY ID
# =========================================================

@medicine_bp.get("/<int:medicine_id>")
def get_one(medicine_id):

    medicine = MedicineService.get_by_id(
        medicine_id
    )

    if not medicine:
        return {
            "success": False,
            "message": "Medicine not found"
        }, 404

    return {
        "success": True,
        "medicine": medicine_to_dict(medicine)
    }


# =========================================================
# UPDATE MEDICINE
# =========================================================

@medicine_bp.put("/<int:medicine_id>")
def update_medicine(medicine_id):

    data = request.get_json(silent=True)

    if not data:
        return {
            "success": False,
            "message": "Request body is required"
        }, 400

    valid, message = validate_medicine(data)

    if not valid:
        return {
            "success": False,
            "message": message
        }, 400

    medicine = MedicineService.update(
        medicine_id,
        data
    )

    if not medicine:
        return {
            "success": False,
            "message": "Medicine not found or invalid data"
        }, 404

    return {
        "success": True,
        "message": "Medicine updated successfully",
        "medicine": medicine_to_dict(medicine)
    }


# =========================================================
# DELETE MEDICINE
# =========================================================

@medicine_bp.delete("/<int:medicine_id>")
def delete_medicine(medicine_id):

    deleted = MedicineService.delete(
        medicine_id
    )

    if not deleted:
        return {
            "success": False,
            "message": "Medicine not found"
        }, 404

    return {
        "success": True,
        "message": "Medicine deleted successfully"
    }


# =========================================================
# SEARCH MEDICINES
# =========================================================

@medicine_bp.get("/search/<string:name>")
def search_medicine(name):

    medicines = MedicineService.search(
        name
    )

    return {
        "success": True,
        "count": len(medicines),
        "medicines": [
            medicine_to_dict(m)
            for m in medicines
        ]
    }


# =========================================================
# LOW STOCK MEDICINES
# =========================================================

@medicine_bp.get("/low-stock")
def low_stock():

    medicines = MedicineService.low_stock()

    return {
        "success": True,
        "count": len(medicines),
        "medicines": [
            medicine_to_dict(m)
            for m in medicines
        ]
    }
# =========================================================
# LOW STOCK MEDICINES BY HOSPITAL
# =========================================================

@medicine_bp.get("/low-stock/hospital/<int:hospital_id>")
def low_stock_by_hospital(hospital_id):

    medicines, error = MedicineService.get_low_stock_by_hospital(
        hospital_id
    )

    if error:
        return {
            "success": False,
            "message": error
        }, 404

    return {
        "success": True,
        "count": len(medicines),
        "medicines": [
            medicine_to_dict(m)
            for m in medicines
        ]
    }