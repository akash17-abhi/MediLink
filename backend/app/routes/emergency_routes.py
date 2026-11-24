from flask import Blueprint, request, jsonify

from app.schemas.emergency_schema import (
    EmergencyCreateSchema,
    EmergencyUpdateSchema,
    AssignAmbulanceSchema,
    AssignHospitalSchema,
)

from app.services.emergency_service import EmergencyService


emergency_bp = Blueprint(
    "emergency",
    __name__,
    url_prefix="/api/emergencies"
)


# =========================================================
# SCHEMAS
# =========================================================

create_schema = EmergencyCreateSchema()
update_schema = EmergencyUpdateSchema()
assign_ambulance_schema = AssignAmbulanceSchema()
assign_hospital_schema = AssignHospitalSchema()


# =========================================================
# HELPER
# =========================================================

def serialize_emergency(emergency):

    return {
        "id": emergency.id,
        "patient_id": emergency.patient_id,
        "hospital_id": emergency.hospital_id,
        "ambulance_id": emergency.ambulance_id,
        "emergency_type": emergency.emergency_type,
        "description": emergency.description,
        "priority": emergency.priority,
        "pickup_location": emergency.pickup_location,
        "destination": emergency.destination,
        "status": emergency.status,
        "created_at": (
            emergency.created_at.strftime("%Y-%m-%d %H:%M:%S")
            if emergency.created_at
            else None
        ),
        "updated_at": (
            emergency.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            if emergency.updated_at
            else None
        ),
    }


def validation_error_response(error):

    return jsonify({
        "success": False,
        "message": "Validation failed",
        "errors": error.messages
    }), 400


# =========================================================
# CREATE EMERGENCY
# =========================================================

@emergency_bp.route("/", methods=["POST"])
def create_emergency():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Request body is required"
            }), 400

        try:
            validated_data = create_schema.load(data)

        except Exception as error:
            return validation_error_response(error)

        emergency, error = EmergencyService.create_emergency(
            validated_data
        )

        if error:
            return jsonify({
                "success": False,
                "message": error
            }), 400

        return jsonify({
            "success": True,
            "message": "Emergency request created successfully",
            "emergency": serialize_emergency(emergency)
        }), 201

    except Exception as error:

        return jsonify({
            "success": False,
            "message": "Failed to create emergency",
            "error": str(error)
        }), 500


# =========================================================
# GET ALL EMERGENCIES
# =========================================================

@emergency_bp.route("/", methods=["GET"])
def get_all_emergencies():

    try:

        emergencies = EmergencyService.get_all_emergencies()

        return jsonify({
            "success": True,
            "count": len(emergencies),
            "emergencies": [
                serialize_emergency(emergency)
                for emergency in emergencies
            ]
        }), 200

    except Exception as error:

        return jsonify({
            "success": False,
            "message": "Failed to fetch emergencies",
            "error": str(error)
        }), 500


# =========================================================
# GET ACTIVE EMERGENCIES
# =========================================================

@emergency_bp.route("/active", methods=["GET"])
def get_active_emergencies():

    try:

        emergencies = EmergencyService.get_active_emergencies()

        return jsonify({
            "success": True,
            "count": len(emergencies),
            "emergencies": [
                serialize_emergency(emergency)
                for emergency in emergencies
            ]
        }), 200

    except Exception as error:

        return jsonify({
            "success": False,
            "message": "Failed to fetch active emergencies",
            "error": str(error)
        }), 500


# =========================================================
# GET PENDING EMERGENCIES
# =========================================================

@emergency_bp.route("/pending", methods=["GET"])
def get_pending_emergencies():

    try:

        emergencies = EmergencyService.get_pending_emergencies()

        return jsonify({
            "success": True,
            "count": len(emergencies),
            "emergencies": [
                serialize_emergency(emergency)
                for emergency in emergencies
            ]
        }), 200


    except Exception as error:

        return jsonify({
            "success": False,
            "message": "Failed to fetch pending emergencies",
            "error": str(error)
        }), 500


# =========================================================
# GET EMERGENCY BY ID
# =========================================================

@emergency_bp.route("/<int:emergency_id>", methods=["GET"])
def get_emergency(emergency_id):

    try:

        emergency, error = EmergencyService.get_emergency(
            emergency_id
        )

        if error:

            return jsonify({
                "success": False,
                "message": error
            }), 404

        return jsonify({
            "success": True,
            "emergency": serialize_emergency(emergency)
        }), 200

    except Exception as error:

        return jsonify({
            "success": False,
            "message": "Failed to fetch emergency",
            "error": str(error)
        }), 500


# =========================================================
# GET PATIENT EMERGENCIES
# =========================================================

@emergency_bp.route(
    "/patient/<int:patient_id>",
    methods=["GET"]
)
def get_patient_emergencies(patient_id):

    try:

        emergencies, error = (
            EmergencyService.get_patient_emergencies(
                patient_id
            )
        )

        if error:

            return jsonify({
                "success": False,
                "message": error
            }), 404

        return jsonify({
            "success": True,
            "count": len(emergencies),
            "emergencies": [
                serialize_emergency(emergency)
                for emergency in emergencies
            ]
        }), 200

    except Exception as error:

        return jsonify({
            "success": False,
            "message": "Failed to fetch patient emergencies",
            "error": str(error)
        }), 500


# =========================================================
# GET HOSPITAL EMERGENCIES
# =========================================================

@emergency_bp.route(
    "/hospital/<int:hospital_id>",
    methods=["GET"]
)
def get_hospital_emergencies(hospital_id):

    try:

        emergencies, error = (
            EmergencyService.get_hospital_emergencies(
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
            "count": len(emergencies),
            "emergencies": [
                serialize_emergency(emergency)
                for emergency in emergencies
            ]
        }), 200

    except Exception as error:

        return jsonify({
            "success": False,
            "message": "Failed to fetch hospital emergencies",
            "error": str(error)
        }), 500


# =========================================================
# ASSIGN HOSPITAL
# =========================================================

@emergency_bp.route(
    "/<int:emergency_id>/assign-hospital",
    methods=["POST"]
)
def assign_hospital(emergency_id):

    try:

        data = request.get_json() or {}

        try:
            validated_data = assign_hospital_schema.load(data)

        except Exception as error:
            return validation_error_response(error)

        emergency, error = EmergencyService.assign_hospital(
            emergency_id,
            validated_data["hospital_id"]
        )

        if error:

            return jsonify({
                "success": False,
                "message": error
            }), 400

        return jsonify({
            "success": True,
            "message": "Hospital assigned successfully",
            "emergency": serialize_emergency(emergency)
        }), 200

    except Exception as error:

        return jsonify({
            "success": False,
            "message": "Failed to assign hospital",
            "error": str(error)
        }), 500


# =========================================================
# ASSIGN AMBULANCE
# =========================================================

@emergency_bp.route(
    "/<int:emergency_id>/assign-ambulance",
    methods=["POST"]
)
def assign_ambulance(emergency_id):

    try:

        data = request.get_json() or {}

        try:
            validated_data = assign_ambulance_schema.load(data)

        except Exception as error:
            return validation_error_response(error)

        emergency, error = EmergencyService.assign_ambulance(
            emergency_id,
            validated_data["ambulance_id"]
        )

        if error:

            return jsonify({
                "success": False,
                "message": error
            }), 400

        return jsonify({
            "success": True,
            "message": "Ambulance assigned successfully",
            "emergency": serialize_emergency(emergency)
        }), 200

    except Exception as error:

        return jsonify({
            "success": False,
            "message": "Failed to assign ambulance",
            "error": str(error)
        }), 500


# =========================================================
# DISPATCH
# =========================================================

@emergency_bp.route(
    "/<int:emergency_id>/dispatch",
    methods=["POST"]
)
def dispatch_emergency(emergency_id):

    try:

        emergency, error = EmergencyService.dispatch(
            emergency_id
        )

        if error:

            return jsonify({
                "success": False,
                "message": error
            }), 400

        return jsonify({
            "success": True,
            "message": "Ambulance dispatched successfully",
            "emergency": serialize_emergency(emergency)
        }), 200

    except Exception as error:

        return jsonify({
            "success": False,
            "message": "Failed to dispatch ambulance",
            "error": str(error)
        }), 500


# =========================================================
# ON THE WAY
# =========================================================

@emergency_bp.route(
    "/<int:emergency_id>/on-the-way",
    methods=["POST"]
)
def on_the_way(emergency_id):

    try:

        emergency, error = EmergencyService.mark_on_the_way(
            emergency_id
        )

        if error:

            return jsonify({
                "success": False,
                "message": error
            }), 400

        return jsonify({
            "success": True,
            "message": "Ambulance marked as on the way",
            "emergency": serialize_emergency(emergency)
        }), 200

    except Exception as error:

        return jsonify({
            "success": False,
            "message": "Failed to update emergency status",
            "error": str(error)
        }), 500


# =========================================================
# ARRIVED
# =========================================================

@emergency_bp.route(
    "/<int:emergency_id>/arrived",
    methods=["POST"]
)
def arrived(emergency_id):

    try:

        emergency, error = EmergencyService.mark_arrived(
            emergency_id
        )

        if error:

            return jsonify({
                "success": False,
                "message": error
            }), 400

        return jsonify({
            "success": True,
            "message": "Ambulance has arrived",
            "emergency": serialize_emergency(emergency)
        }), 200

    except Exception as error:

        return jsonify({
            "success": False,
            "message": "Failed to update emergency status",
            "error": str(error)
        }), 500


# =========================================================
# PATIENT PICKED UP
# =========================================================

@emergency_bp.route(
    "/<int:emergency_id>/patient-picked-up",
    methods=["POST"]
)
def patient_picked_up(emergency_id):

    try:

        emergency, error = (
            EmergencyService.mark_patient_picked_up(
                emergency_id
            )
        )

        if error:

            return jsonify({
                "success": False,
                "message": error
            }), 400

        return jsonify({
            "success": True,
            "message": "Patient picked up successfully",
            "emergency": serialize_emergency(emergency)
        }), 200

    except Exception as error:

        return jsonify({
            "success": False,
            "message": "Failed to update emergency status",
            "error": str(error)
        }), 500


# =========================================================
# HOSPITAL ARRIVAL
# =========================================================

@emergency_bp.route(
    "/<int:emergency_id>/hospital-arrived",
    methods=["POST"]
)
def hospital_arrived(emergency_id):

    try:

        emergency, error = (
            EmergencyService.mark_hospital_arrived(
                emergency_id
            )
        )

        if error:

            return jsonify({
                "success": False,
                "message": error
            }), 400

        return jsonify({
            "success": True,
            "message": "Ambulance arrived at hospital",
            "emergency": serialize_emergency(emergency)
        }), 200

    except Exception as error:

        return jsonify({
            "success": False,
            "message": "Failed to update emergency status",
            "error": str(error)
        }), 500


# =========================================================
# COMPLETE
# =========================================================

@emergency_bp.route(
    "/<int:emergency_id>/complete",
    methods=["POST"]
)
def complete_emergency(emergency_id):

    try:

        emergency, error = (
            EmergencyService.complete_emergency(
                emergency_id
            )
        )

        if error:

            return jsonify({
                "success": False,
                "message": error
            }), 400

        return jsonify({
            "success": True,
            "message": "Emergency completed successfully",
            "emergency": serialize_emergency(emergency)
        }), 200

    except Exception as error:

        return jsonify({
            "success": False,
            "message": "Failed to complete emergency",
            "error": str(error)
        }), 500


# =========================================================
# CANCEL
# =========================================================

@emergency_bp.route(
    "/<int:emergency_id>/cancel",
    methods=["POST"]
)
def cancel_emergency(emergency_id):

    try:

        emergency, error = (
            EmergencyService.cancel_emergency(
                emergency_id
            )
        )

        if error:

            return jsonify({
                "success": False,
                "message": error
            }), 400

        return jsonify({
            "success": True,
            "message": "Emergency cancelled successfully",
            "emergency": serialize_emergency(emergency)
        }), 200

    except Exception as error:

        return jsonify({
            "success": False,
            "message": "Failed to cancel emergency",
            "error": str(error)
        }), 500