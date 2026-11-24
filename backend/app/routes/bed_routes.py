from flask import Blueprint, request, jsonify

from app.schemas.bed_schema import (
    BedCreateSchema,
    BedUpdateSchema,
    BedStatusSchema,
    BedAssignPatientSchema,
)

from app.services.bed_service import BedService


# =========================================================
# BLUEPRINT
# =========================================================

bed_bp = Blueprint(
    "bed",
    __name__,
    url_prefix="/api/beds"
)


# =========================================================
# SCHEMAS
# =========================================================

bed_create_schema = BedCreateSchema()
bed_update_schema = BedUpdateSchema()
bed_status_schema = BedStatusSchema()
bed_assign_patient_schema = BedAssignPatientSchema()


# =========================================================
# HELPER
# =========================================================

def serialize_bed(bed):
    """
    Convert Bed model into JSON-safe dictionary.
    """

    if hasattr(bed, "to_dict"):
        return bed.to_dict()

    return {
        "id": bed.id,
        "hospital_id": bed.hospital_id,
        "bed_number": bed.bed_number,
        "ward": bed.ward,
        "bed_type": bed.bed_type,
        "floor": bed.floor,
        "room_number": bed.room_number,
        "status": bed.status,
        "patient_id": bed.patient_id,
        "notes": bed.notes,
        "created_at": (
            bed.created_at.strftime("%Y-%m-%d %H:%M:%S")
            if bed.created_at
            else None
        ),
        "updated_at": (
            bed.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            if bed.updated_at
            else None
        ),
    }


# =========================================================
# CREATE BED
# =========================================================

@bed_bp.route("/", methods=["POST"])
def create_bed():

    data = request.get_json(silent=True) or {}

    try:
        validated_data = bed_create_schema.load(data)

    except Exception as e:

        return jsonify({
            "success": False,
            "message": "Invalid bed data",
            "errors": str(e)
        }), 400

    bed, error = BedService.create_bed(
        validated_data
    )

    if error:

        return jsonify({
            "success": False,
            "message": error
        }), 400

    return jsonify({
        "success": True,
        "message": "Bed created successfully",
        "bed": serialize_bed(bed)
    }), 201


# =========================================================
# GET ALL BEDS
# =========================================================

@bed_bp.route("/", methods=["GET"])
def get_all_beds():

    beds, error = BedService.get_all_beds()

    if error:

        return jsonify({
            "success": False,
            "message": error
        }), 400

    return jsonify({
        "success": True,
        "count": len(beds),
        "beds": [
            serialize_bed(bed)
            for bed in beds
        ]
    }), 200


# =========================================================
# GET ONE BED
# =========================================================

@bed_bp.route("/<int:bed_id>", methods=["GET"])
def get_bed(bed_id):

    bed, error = BedService.get_bed(
        bed_id
    )

    if error:

        return jsonify({
            "success": False,
            "message": error
        }), 404

    return jsonify({
        "success": True,
        "bed": serialize_bed(bed)
    }), 200


# =========================================================
# GET HOSPITAL BEDS
# =========================================================

@bed_bp.route(
    "/hospital/<int:hospital_id>",
    methods=["GET"]
)
def get_hospital_beds(hospital_id):

    beds, error = BedService.get_hospital_beds(
        hospital_id
    )

    if error:

        return jsonify({
            "success": False,
            "message": error
        }), 404

    return jsonify({
        "success": True,
        "hospital_id": hospital_id,
        "count": len(beds),
        "beds": [
            serialize_bed(bed)
            for bed in beds
        ]
    }), 200


# =========================================================
# GET AVAILABLE BEDS
# =========================================================

@bed_bp.route("/available", methods=["GET"])
def get_available_beds():

    beds, error = BedService.get_available_beds()

    if error:

        return jsonify({
            "success": False,
            "message": error
        }), 400

    return jsonify({
        "success": True,
        "count": len(beds),
        "beds": [
            serialize_bed(bed)
            for bed in beds
        ]
    }), 200


# =========================================================
# GET AVAILABLE BEDS BY HOSPITAL
# =========================================================

@bed_bp.route(
    "/available/hospital/<int:hospital_id>",
    methods=["GET"]
)
def get_available_hospital_beds(hospital_id):

    beds, error = (
        BedService.get_available_hospital_beds(
            hospital_id
        )
    )

    if error:

        return jsonify({
            "success": False,
            "message": error
        }), 404

    return jsonify({
        "success": True,
        "hospital_id": hospital_id,
        "count": len(beds),
        "beds": [
            serialize_bed(bed)
            for bed in beds
        ]
    }), 200


# =========================================================
# GET AVAILABLE BEDS BY TYPE
# =========================================================

@bed_bp.route("/available/type/<string:bed_type>", methods=["GET"])
def get_available_beds_by_type(bed_type):

    hospital_id = request.args.get(
        "hospital_id",
        type=int
    )

    beds, error = (
        BedService.get_available_beds_by_type(
            bed_type,
            hospital_id
        )
    )

    if error:

        return jsonify({
            "success": False,
            "message": error
        }), 404

    return jsonify({
        "success": True,
        "bed_type": bed_type,
        "hospital_id": hospital_id,
        "count": len(beds),
        "beds": [
            serialize_bed(bed)
            for bed in beds
        ]
    }), 200


# =========================================================
# UPDATE BED
# =========================================================

@bed_bp.route(
    "/<int:bed_id>",
    methods=["PUT"]
)
def update_bed(bed_id):

    data = request.get_json(silent=True) or {}

    try:
        validated_data = bed_update_schema.load(data)

    except Exception as e:

        return jsonify({
            "success": False,
            "message": "Invalid bed data",
            "errors": str(e)
        }), 400

    bed, error = BedService.update_bed(
        bed_id,
        validated_data
    )

    if error:

        return jsonify({
            "success": False,
            "message": error
        }), 400

    return jsonify({
        "success": True,
        "message": "Bed updated successfully",
        "bed": serialize_bed(bed)
    }), 200


# =========================================================
# DELETE BED
# =========================================================

@bed_bp.route(
    "/<int:bed_id>",
    methods=["DELETE"]
)
def delete_bed(bed_id):

    result, error = BedService.delete_bed(
        bed_id
    )

    if error:

        return jsonify({
            "success": False,
            "message": error
        }), 400

    return jsonify({
        "success": True,
        "message": "Bed deleted successfully"
    }), 200


# =========================================================
# ASSIGN PATIENT
# =========================================================

@bed_bp.route(
    "/<int:bed_id>/assign-patient",
    methods=["POST"]
)
def assign_patient(bed_id):

    data = request.get_json(silent=True) or {}

    try:
        validated_data = (
            bed_assign_patient_schema.load(data)
        )

    except Exception as e:

        return jsonify({
            "success": False,
            "message": "Invalid patient assignment data",
            "errors": str(e)
        }), 400

    bed, error = BedService.assign_patient(
        bed_id,
        validated_data["patient_id"]
    )

    if error:

        return jsonify({
            "success": False,
            "message": error
        }), 400

    return jsonify({
        "success": True,
        "message": "Patient assigned to bed successfully",
        "bed": serialize_bed(bed)
    }), 200


# =========================================================
# RELEASE BED
# =========================================================

@bed_bp.route(
    "/<int:bed_id>/release",
    methods=["POST"]
)
def release_bed(bed_id):

    bed, error = BedService.release_bed(
        bed_id
    )

    if error:

        return jsonify({
            "success": False,
            "message": error
        }), 400

    return jsonify({
        "success": True,
        "message": "Bed released successfully",
        "bed": serialize_bed(bed)
    }), 200


# =========================================================
# UPDATE BED STATUS
# =========================================================

@bed_bp.route(
    "/<int:bed_id>/status",
    methods=["PATCH"]
)
def update_bed_status(bed_id):

    data = request.get_json(silent=True) or {}

    try:
        validated_data = (
            bed_status_schema.load(data)
        )

    except Exception as e:

        return jsonify({
            "success": False,
            "message": "Invalid bed status",
            "errors": str(e)
        }), 400

    bed, error = BedService.update_status(
        bed_id,
        validated_data["status"]
    )

    if error:

        return jsonify({
            "success": False,
            "message": error
        }), 400

    return jsonify({
        "success": True,
        "message": "Bed status updated successfully",
        "bed": serialize_bed(bed)
    }), 200


# =========================================================
# BED STATISTICS
# =========================================================

@bed_bp.route(
    "/statistics",
    methods=["GET"]
)
def get_bed_statistics():

    hospital_id = request.args.get(
        "hospital_id",
        type=int
    )

    statistics, error = (
        BedService.get_statistics(
            hospital_id
        )
    )

    if error:

        return jsonify({
            "success": False,
            "message": error
        }), 404

    return jsonify({
        "success": True,
        "hospital_id": hospital_id,
        "statistics": statistics
    }), 200