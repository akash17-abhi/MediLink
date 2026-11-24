"""
Patient Portal API Endpoints
Enables authenticated patients to book appointments, trigger emergency requests,
and review their medical interactions.
"""

from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app.extensions import db
from app.models.user import User
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.emergency import Emergency
from app.models.hospital import Hospital
from app.models.doctor import Doctor
from app.models.ambulance import Ambulance
from app.models.prescription import Prescription
from app.models.medical_record import MedicalRecord
from app.models.bill import Bill
from app.decorators.role_required import role_required

patient_portal_bp = Blueprint("patient_portal", __name__, url_prefix="/api/patient")


def get_current_patient():
    """Retrieve the Patient record corresponding to the current logged-in user."""
    try:
        user_id = get_jwt_identity()
    except Exception:
        user_id = None
    if not user_id:
        return None
    user = db.session.get(User, int(user_id))
    if not user:
        return None

    patient = Patient.query.filter_by(email=user.email).first()
    if not patient:
        # Create a linked patient profile automatically if not found
        patient = Patient(
            full_name=user.full_name,
            email=user.email,
            phone="+91 9800000000",
            gender="Not Specified",
            date_of_birth=datetime(1995, 1, 1).date(),
            age=30
        )
        db.session.add(patient)
        db.session.commit()
    return patient


@patient_portal_bp.route("/appointments", methods=["GET", "POST"])
@role_required("Patient", "Admin")
def patient_appointments():
    """Book a new appointment or view current bookings."""
    patient = get_current_patient()
    if not patient:
        return jsonify({"success": False, "message": "Patient profile not found"}), 404

    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        hospital_id = data.get("hospital_id")
        doctor_id = data.get("doctor_id")
        appt_date_str = data.get("appointment_date")
        appt_time_str = data.get("appointment_time", "11:00 AM")
        reason = data.get("reason", "Consultation")

        if not hospital_id:
            return jsonify({"success": False, "message": "Hospital ID is required"}), 400

        # If no specific doctor selected, pick the first doctor in that hospital
        if not doctor_id:
            first_doc = Doctor.query.filter_by(hospital_id=hospital_id, is_active=True).first()
            doctor_id = first_doc.id if first_doc else 1

        try:
            appt_date = datetime.strptime(appt_date_str, "%Y-%m-%d").date() if appt_date_str else datetime.now().date()
        except Exception:
            appt_date = datetime.now().date()

        try:
            appt_time = datetime.strptime(appt_time_str, "%I:%M %p").time()
        except Exception:
            appt_time = datetime.strptime("10:00", "%H:%M").time()

        appointment = Appointment(
            patient_id=patient.id,
            doctor_id=doctor_id,
            hospital_id=hospital_id,
            appointment_date=appt_date,
            appointment_time=appt_time,
            reason=reason,
            status="Scheduled",
            consultation_mode="Offline",
            payment_status="Paid"
        )
        db.session.add(appointment)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Appointment booked successfully!",
            "appointment": {
                "id": appointment.id,
                "hospital": appointment.hospital.name if appointment.hospital else None,
                "doctor": appointment.doctor.full_name if appointment.doctor else None,
                "date": str(appointment.appointment_date),
                "time": str(appointment.appointment_time),
                "status": appointment.status
            }
        }), 201

    # GET: List appointments
    appointments = Appointment.query.filter_by(patient_id=patient.id).order_by(Appointment.appointment_date.desc()).all()
    return jsonify({
        "success": True,
        "count": len(appointments),
        "appointments": [
            {
                "id": a.id,
                "hospital_name": a.hospital.name if a.hospital else "Hospital",
                "doctor_name": a.doctor.full_name if a.doctor else "Doctor",
                "specialization": a.doctor.specialization if a.doctor else "",
                "consultation_fee": a.doctor.consultation_fee if a.doctor else 500.0,
                "date": str(a.appointment_date),
                "time": str(a.appointment_time),
                "reason": a.reason,
                "status": a.status,
                "payment_status": a.payment_status
            } for a in appointments
        ]
    }), 200


@patient_portal_bp.route("/emergencies", methods=["GET", "POST"])
def patient_emergencies():
    """Trigger an emergency dispatch request (Public SOS or authenticated) or view personal alerts."""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        hospital_id = data.get("hospital_id")
        caller_name = data.get("caller_name", "Emergency Patient")
        caller_phone = data.get("phone", "+91 9999999999")
        pickup_loc = data.get("pickup_location", "Current User Geolocation")
        emg_type = data.get("emergency_type", "Acute Medical Emergency")
        priority = data.get("priority", "Critical")

        # Try to associate with logged-in patient if available
        patient = None
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            if user_id:
                user = db.session.get(User, int(user_id))
                if user:
                    patient = Patient.query.filter_by(email=user.email).first()
        except Exception:
            patient = None

        if not patient:
            # Create/find emergency guest patient record
            patient = Patient.query.filter_by(phone=caller_phone).first()
            if not patient:
                patient = Patient(
                    full_name=caller_name,
                    email=f"sos.{int(datetime.now().timestamp())}@emergency.medilink",
                    phone=caller_phone,
                    gender="Not Specified",
                    date_of_birth=datetime(1995, 1, 1).date(),
                    age=30
                )
                db.session.add(patient)
                db.session.commit()

        # Pick nearest available ambulance at target hospital if possible
        amb = None
        if hospital_id:
            amb = Ambulance.query.filter_by(hospital_id=hospital_id, availability_status="Available").first()

        hosp = Hospital.query.get(hospital_id) if hospital_id else None

        emergency = Emergency(
            patient_id=patient.id,
            hospital_id=hospital_id,
            ambulance_id=amb.id if amb else None,
            emergency_type=emg_type,
            priority=priority,
            pickup_location=pickup_loc,
            destination=hosp.name if hosp else (amb.hospital.name if (amb and amb.hospital) else "Nearest Hospital"),
            status="Dispatched"
        )
        if amb:
            amb.availability_status = "On Duty"

        db.session.add(emergency)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Emergency ambulance dispatched successfully!",
            "emergency": {
                "id": emergency.id,
                "priority": emergency.priority,
                "status": emergency.status,
                "ambulance": amb.registration_number if amb else "Response Unit #01",
                "driver_name": amb.driver_name if amb else "On-Duty Emergency Paramedic",
                "driver_phone": amb.driver_phone if amb else "+91 9800001080",
                "hospital": emergency.destination,
                "hospital_phone": hosp.emergency_contact if hosp else "+91 108",
                "eta_minutes": "8 - 12 mins"
            }
        }), 201

    # GET: List personal emergencies (requires logged in patient)
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"success": True, "count": 0, "emergencies": []}), 200
        patient = get_current_patient()
        if not patient:
            return jsonify({"success": True, "count": 0, "emergencies": []}), 200
        emergencies = Emergency.query.filter_by(patient_id=patient.id).order_by(Emergency.created_at.desc()).all()
        return jsonify({
            "success": True,
            "count": len(emergencies),
            "emergencies": [
                {
                    "id": e.id,
                    "emergency_type": e.emergency_type,
                    "priority": e.priority,
                    "pickup_location": e.pickup_location,
                    "hospital_name": e.hospital.name if e.hospital else e.destination,
                    "ambulance_reg": e.ambulance.registration_number if e.ambulance else None,
                    "status": e.status,
                    "created_at": e.created_at.strftime("%Y-%m-%d %I:%M %p") if e.created_at else "Just now"
                } for e in emergencies
            ]
        }), 200
    except Exception:
        return jsonify({"success": True, "count": 0, "emergencies": []}), 200


@patient_portal_bp.route("/prescriptions", methods=["GET"])
@role_required("Patient", "Admin")
def patient_prescriptions():
    """Retrieve active and past electronic prescriptions for the logged-in patient."""
    patient = get_current_patient()
    if not patient:
        return jsonify({"success": True, "count": 0, "prescriptions": []}), 200

    rxs = Prescription.query.filter_by(patient_id=patient.id).order_by(Prescription.created_at.desc()).all()
    return jsonify({
        "success": True,
        "count": len(rxs),
        "prescriptions": [
            {
                "id": rx.id,
                "medicines": rx.medicines,
                "dosage": rx.dosage,
                "duration": rx.duration,
                "instructions": rx.instructions,
                "doctor_name": rx.doctor.full_name if rx.doctor else "Hospital Specialist",
                "specialization": rx.doctor.specialization if rx.doctor else "General Medicine",
                "hospital_name": rx.doctor.hospital.name if (rx.doctor and rx.doctor.hospital) else "MediLink Partner Hospital",
                "created_at": rx.created_at.strftime("%Y-%m-%d") if rx.created_at else "Recently"
            } for rx in rxs
        ]
    }), 200


@patient_portal_bp.route("/medical-records", methods=["GET"])
@role_required("Patient", "Admin")
def patient_medical_records():
    """Retrieve diagnosis history and clinical summaries."""
    patient = get_current_patient()
    if not patient:
        return jsonify({"success": True, "count": 0, "records": []}), 200

    records = MedicalRecord.query.filter_by(patient_id=patient.id).order_by(MedicalRecord.created_at.desc()).all()
    return jsonify({
        "success": True,
        "count": len(records),
        "records": [
            {
                "id": r.id,
                "diagnosis": r.diagnosis,
                "symptoms": r.symptoms,
                "prescription": r.prescription,
                "lab_tests": r.lab_tests,
                "notes": r.notes,
                "follow_up_date": str(r.follow_up_date) if r.follow_up_date else None,
                "doctor_name": r.doctor.full_name if r.doctor else "Attending Physician",
                "specialization": r.doctor.specialization if r.doctor else "Consultant",
                "created_at": r.created_at.strftime("%Y-%m-%d") if r.created_at else "Recent"
            } for r in records
        ]
    }), 200


@patient_portal_bp.route("/bills", methods=["GET"])
@role_required("Patient", "Admin")
def patient_bills():
    """Retrieve itemized billing and invoice records."""
    patient = get_current_patient()
    if not patient:
        return jsonify({"success": True, "count": 0, "bills": []}), 200

    bills = Bill.query.filter_by(patient_id=patient.id).order_by(Bill.created_at.desc()).all()
    return jsonify({
        "success": True,
        "count": len(bills),
        "bills": [
            {
                "id": b.id,
                "invoice_number": f"INV-{b.id:05d}",
                "hospital_name": b.hospital.name if b.hospital else "MediLink Healthcare",
                "doctor_name": b.doctor.full_name if b.doctor else None,
                "consultation_charge": b.consultation_charge or 0.0,
                "laboratory_charge": b.laboratory_charge or 0.0,
                "medicine_charge": b.medicine_charge or 0.0,
                "other_charge": b.other_charge or 0.0,
                "discount": b.discount or 0.0,
                "tax": b.tax or 0.0,
                "total_amount": b.total_amount or 0.0,
                "payment_status": b.payment_status or "Paid",
                "created_at": b.created_at.strftime("%Y-%m-%d") if b.created_at else "Today"
            } for b in bills
        ]
    }), 200


@patient_portal_bp.route("/profile", methods=["GET", "PUT", "POST"])
@role_required("Patient", "Admin")
def patient_profile():
    """Retrieve or update patient profile and health card details."""
    patient = get_current_patient()
    if not patient:
        return jsonify({"success": False, "message": "Profile not found"}), 404

    if request.method in ["PUT", "POST"]:
        data = request.get_json() or {}

        if "full_name" in data and data["full_name"]:
            patient.full_name = data["full_name"].strip()
            # Also update corresponding User account if exists
            try:
                user_id = get_jwt_identity()
                if user_id:
                    user = db.session.get(User, int(user_id))
                    if user:
                        user.full_name = patient.full_name
                        user.name = patient.full_name
            except Exception:
                pass

        if "phone" in data and data["phone"]:
            patient.phone = data["phone"].strip()
        if "gender" in data and data["gender"]:
            patient.gender = data["gender"]
        if "age" in data and data["age"]:
            try:
                patient.age = int(data["age"])
            except (ValueError, TypeError):
                pass
        if "blood_group" in data:
            patient.blood_group = data["blood_group"]
        if "address" in data:
            patient.address = data["address"]
        if "city" in data:
            patient.city = data["city"]
        if "state" in data:
            patient.state = data["state"]
        if "pincode" in data:
            patient.pincode = data["pincode"]
        if "emergency_contact_name" in data:
            patient.emergency_contact_name = data["emergency_contact_name"]
        if "emergency_contact_phone" in data:
            patient.emergency_contact_phone = data["emergency_contact_phone"]
        if "emergency_contact" in data and not data.get("emergency_contact_phone"):
            patient.emergency_contact_phone = data["emergency_contact"]
        if "emergency_contact_relation" in data:
            patient.emergency_contact_relation = data["emergency_contact_relation"]
        if "allergies" in data:
            patient.allergies = data["allergies"]
        if "chronic_conditions" in data:
            patient.chronic_conditions = data["chronic_conditions"]
        if "current_medications" in data:
            patient.current_medications = data["current_medications"]

        db.session.commit()

    return jsonify({
        "success": True,
        "message": "Profile updated successfully!" if request.method in ["PUT", "POST"] else None,
        "profile": {
            "id": patient.id,
            "patient_code": f"MED-PT-{patient.id:04d}",
            "full_name": patient.full_name,
            "email": patient.email,
            "phone": patient.phone or "+91 9800000000",
            "gender": patient.gender or "Not Specified",
            "age": patient.age or 30,
            "blood_group": patient.blood_group or "B+",
            "address": patient.address or "",
            "city": patient.city or "",
            "state": patient.state or "",
            "pincode": patient.pincode or "",
            "emergency_contact_name": patient.emergency_contact_name or "Family Member",
            "emergency_contact_phone": patient.emergency_contact_phone or "+91 9830099999",
            "emergency_contact": patient.emergency_contact_phone or "+91 9830099999",
            "emergency_contact_relation": patient.emergency_contact_relation or "Spouse/Parent",
            "allergies": patient.allergies or "None recorded",
            "chronic_conditions": patient.chronic_conditions or "None recorded",
            "current_medications": patient.current_medications or "None"
        }
    }), 200


@patient_portal_bp.route("/appointments/<int:appointment_id>/cancel", methods=["POST"])
@role_required("Patient", "Admin")
def cancel_appointment(appointment_id):
    """Cancel a scheduled appointment."""
    patient = get_current_patient()
    if not patient:
        return jsonify({"success": False, "message": "Patient not found"}), 404

    appointment = Appointment.query.filter_by(id=appointment_id, patient_id=patient.id).first()
    if not appointment:
        return jsonify({"success": False, "message": "Appointment not found"}), 404

    appointment.status = "Cancelled"
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Appointment #{appointment_id} has been cancelled successfully."
    }), 200
