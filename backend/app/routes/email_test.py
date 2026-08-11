# backend/app/routes/email_test.py

from flask import Blueprint, request, jsonify

from app.services.email_service import EmailService


email_test_bp = Blueprint(
    "email_test",
    __name__,
    url_prefix="/api/email"
)


@email_test_bp.route("/test", methods=["POST"])
def test_email():

    data = request.get_json(silent=True) or {}

    recipient = data.get("email")

    if not recipient:
        return jsonify({
            "success": False,
            "message": "Email address is required"
        }), 400

    success, error = EmailService.send_test_email(
        recipient
    )

    if not success:
        return jsonify({
            "success": False,
            "message": "Failed to send test email",
            "error": error
        }), 500

    return jsonify({
        "success": True,
        "message": "Test email sent successfully",
        "recipient": recipient
    }), 200


@email_test_bp.route(
    "/appointment-confirmation",
    methods=["POST"]
)
def appointment_confirmation_email():

    data = request.get_json(silent=True) or {}

    required_fields = [
        "patient_email",
        "patient_name",
        "doctor_name",
        "appointment_date",
        "appointment_time"
    ]

    missing_fields = [
        field
        for field in required_fields
        if not data.get(field)
    ]

    if missing_fields:
        return jsonify({
            "success": False,
            "message": "Required fields are missing",
            "missing_fields": missing_fields
        }), 400

    success, error = (
        EmailService.send_appointment_confirmation(
            patient_email=data["patient_email"],
            patient_name=data["patient_name"],
            doctor_name=data["doctor_name"],
            appointment_date=data["appointment_date"],
            appointment_time=data["appointment_time"],
            hospital_name=data.get("hospital_name")
        )
    )

    if not success:
        return jsonify({
            "success": False,
            "message": "Failed to send appointment confirmation email",
            "error": error
        }), 500

    return jsonify({
        "success": True,
        "message": "Appointment confirmation email sent successfully",
        "recipient": data["patient_email"]
    }), 200


@email_test_bp.route(
    "/appointment-cancellation",
    methods=["POST"]
)
def appointment_cancellation_email():

    data = request.get_json(silent=True) or {}

    required_fields = [
        "patient_email",
        "patient_name",
        "doctor_name",
        "appointment_date",
        "appointment_time"
    ]

    missing_fields = [
        field
        for field in required_fields
        if not data.get(field)
    ]

    if missing_fields:
        return jsonify({
            "success": False,
            "message": "Required fields are missing",
            "missing_fields": missing_fields
        }), 400

    success, error = (
        EmailService.send_appointment_cancellation(
            patient_email=data["patient_email"],
            patient_name=data["patient_name"],
            doctor_name=data["doctor_name"],
            appointment_date=data["appointment_date"],
            appointment_time=data["appointment_time"],
            reason=data.get("reason")
        )
    )

    if not success:
        return jsonify({
            "success": False,
            "message": "Failed to send appointment cancellation email",
            "error": error
        }), 500

    return jsonify({
        "success": True,
        "message": "Appointment cancellation email sent successfully",
        "recipient": data["patient_email"]
    }), 200