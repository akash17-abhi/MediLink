"""
Hospital / Clinic Portal API Routes
Protected by @role_required("Hospital", "Admin")
Provides comprehensive bed management, ambulance fleet controls,
emergency triage, and appointment scheduling.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
from app.decorators.role_required import role_required
from app.extensions import db
from app.models.hospital import Hospital
from app.models.bed import Bed
from app.models.ambulance import Ambulance
from app.models.emergency import Emergency
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.medical_record import MedicalRecord
from app.models.prescription import Prescription
from app.services.recommendation_service import RecommendationService

hospital_admin_bp = Blueprint("hospital_admin", __name__, url_prefix="/api/hospital-admin")


def get_current_hospital():
    """Find the hospital associated with the logged-in hospital admin user."""
    user_id = get_jwt_identity()
    hospital = Hospital.query.filter_by(user_id=int(user_id)).first()
    if not hospital:
        # Fallback to the first hospital for demo purposes if not explicitly bound
        hospital = Hospital.query.first()
    return hospital


@hospital_admin_bp.route("/summary", methods=["GET"])
@role_required("Hospital", "Admin")
def hospital_summary():
    """KPI summary of the hospital's live beds, fleet, emergencies, and appointments."""
    h = get_current_hospital()
    if not h:
        return jsonify({"success": False, "message": "Hospital profile not found"}), 404

    bed_summary = RecommendationService.get_hospital_bed_summary(h.id)
    ambulances = Ambulance.query.filter_by(hospital_id=h.id).all()
    emergencies = Emergency.query.filter_by(hospital_id=h.id).all()
    appointments = Appointment.query.filter_by(hospital_id=h.id).all()
    doctors = Doctor.query.filter_by(hospital_id=h.id).all()

    active_emergencies = [e for e in emergencies if e.status in ["Requested", "Dispatched", "Arrived"]]
    avail_ambulances = [a for a in ambulances if a.availability_status.lower() == "available"]

    return jsonify({
        "success": True,
        "hospital": {
            "id": h.id,
            "name": h.name,
            "registration_number": h.registration_number,
            "city": h.city,
            "phone": h.phone,
            "emergency_contact": h.emergency_contact
        },
        "beds": bed_summary,
        "ambulances": {
            "total": len(ambulances),
            "available": len(avail_ambulances)
        },
        "emergencies": {
            "total": len(emergencies),
            "active": len(active_emergencies)
        },
        "appointments": {
            "total": len(appointments),
            "scheduled": sum(1 for a in appointments if a.status in ["Scheduled", "Pending", "Confirmed"])
        },
        "doctors_count": len(doctors)
    }), 200


@hospital_admin_bp.route("/beds", methods=["GET"])
@role_required("Hospital", "Admin")
def list_beds():
    """List all beds for this hospital with optional bed_type filter."""
    h = get_current_hospital()
    bed_type = request.args.get("bed_type")

    query = Bed.query.filter_by(hospital_id=h.id)
    if bed_type:
        query = query.filter(Bed.bed_type.ilike(f"%{bed_type}%"))

    beds = query.order_by(Bed.bed_type.asc(), Bed.bed_number.asc()).all()

    return jsonify({
        "success": True,
        "hospital_id": h.id,
        "count": len(beds),
        "beds": [
            {
                "id": b.id,
                "bed_number": b.bed_number,
                "ward": b.ward,
                "bed_type": b.bed_type,
                "floor": b.floor,
                "room_number": b.room_number,
                "status": b.status,
                "notes": b.notes
            } for b in beds
        ]
    }), 200


@hospital_admin_bp.route("/beds/<int:bed_id>", methods=["PUT", "PATCH"])
@role_required("Hospital", "Admin")
def update_bed(bed_id):
    """Update a single bed's status and notes."""
    h = get_current_hospital()
    bed = Bed.query.filter_by(id=bed_id, hospital_id=h.id).first()
    if not bed:
        return jsonify({"success": False, "message": "Bed not found in this facility"}), 404

    data = request.get_json(silent=True) or {}
    if "status" in data:
        bed.status = data["status"]
    if "notes" in data:
        bed.notes = data["notes"]

    db.session.commit()
    return jsonify({
        "success": True,
        "message": f"Bed {bed.bed_number} updated to {bed.status}",
        "bed": {
            "id": bed.id,
            "bed_number": bed.bed_number,
            "status": bed.status,
            "bed_type": bed.bed_type
        }
    }), 200


@hospital_admin_bp.route("/beds/quick-toggle", methods=["POST"])
@role_required("Hospital", "Admin")
def quick_toggle_bed():
    """Quickly toggle the status of the first available or occupied bed of a given type."""
    h = get_current_hospital()
    data = request.get_json(silent=True) or {}
    bed_type = data.get("bed_type", "ICU")
    action = data.get("action", "occupy")  # 'occupy' or 'release'

    if action == "occupy":
        target = Bed.query.filter_by(hospital_id=h.id, bed_type=bed_type, status="Available").first()
        if not target:
            return jsonify({"success": False, "message": f"No available {bed_type} beds to occupy"}), 400
        target.status = "Occupied"
    else:
        target = Bed.query.filter_by(hospital_id=h.id, bed_type=bed_type, status="Occupied").first()
        if not target:
            return jsonify({"success": False, "message": f"No occupied {bed_type} beds to release"}), 400
        target.status = "Available"

    db.session.commit()
    return jsonify({
        "success": True,
        "message": f"{bed_type} Bed {target.bed_number} is now {target.status}",
        "bed": {
            "id": target.id,
            "bed_number": target.bed_number,
            "bed_type": target.bed_type,
            "status": target.status
        }
    }), 200


@hospital_admin_bp.route("/ambulances", methods=["GET"])
@role_required("Hospital", "Admin")
def list_ambulances():
    """List all ambulances assigned to this hospital."""
    h = get_current_hospital()
    ambulances = Ambulance.query.filter_by(hospital_id=h.id).all()
    return jsonify({
        "success": True,
        "count": len(ambulances),
        "ambulances": [
            {
                "id": a.id,
                "registration_number": a.registration_number,
                "ambulance_type": a.ambulance_type,
                "driver_name": a.driver_name,
                "driver_phone": a.driver_phone,
                "current_location": a.current_location,
                "availability_status": a.availability_status,
                "emergency_status": a.emergency_status
            } for a in ambulances
        ]
    }), 200


@hospital_admin_bp.route("/ambulances/<int:amb_id>", methods=["PUT", "PATCH"])
@role_required("Hospital", "Admin")
def update_ambulance(amb_id):
    """Update ambulance availability or emergency status."""
    h = get_current_hospital()
    amb = Ambulance.query.filter_by(id=amb_id, hospital_id=h.id).first()
    if not amb:
        return jsonify({"success": False, "message": "Ambulance not found in this facility"}), 404

    data = request.get_json(silent=True) or {}
    if "availability_status" in data:
        amb.availability_status = data["availability_status"]
    if "emergency_status" in data:
        amb.emergency_status = data["emergency_status"]
    if "current_location" in data:
        amb.current_location = data["current_location"]

    db.session.commit()
    return jsonify({
        "success": True,
        "message": f"Ambulance {amb.registration_number} status updated to {amb.availability_status}",
        "ambulance": {
            "id": amb.id,
            "registration_number": amb.registration_number,
            "availability_status": amb.availability_status
        }
    }), 200


@hospital_admin_bp.route("/emergencies", methods=["GET", "PATCH"])
@role_required("Hospital", "Admin")
def manage_emergencies():
    """Get or update emergency dispatch requests for this hospital."""
    h = get_current_hospital()

    if request.method == "PATCH":
        data = request.get_json(silent=True) or {}
        emergency_id = data.get("emergency_id")
        emg = Emergency.query.filter_by(id=emergency_id, hospital_id=h.id).first()
        if not emg:
            return jsonify({"success": False, "message": "Emergency alert not found"}), 404

        new_status = data.get("status")
        if new_status:
            emg.status = new_status
            db.session.commit()
            return jsonify({"success": True, "message": f"Emergency #{emg.id} status updated to {emg.status}"}), 200

    emergencies = Emergency.query.filter_by(hospital_id=h.id).order_by(Emergency.created_at.desc()).all()
    return jsonify({
        "success": True,
        "count": len(emergencies),
        "emergencies": [
            {
                "id": e.id,
                "patient_id": e.patient_id,
                "patient_name": e.patient.full_name if e.patient else "Emergency Patient",
                "emergency_type": e.emergency_type,
                "priority": e.priority,
                "pickup_location": e.pickup_location,
                "destination": e.destination,
                "status": e.status,
                "ambulance_reg": e.ambulance.registration_number if e.ambulance else None,
                "created_at": e.created_at.strftime("%Y-%m-%d %H:%M:%S") if e.created_at else None
            } for e in emergencies
        ]
    }), 200


@hospital_admin_bp.route("/appointments", methods=["GET", "PATCH"])
@role_required("Hospital", "Admin")
def manage_appointments():
    """Get or update patient appointments for this hospital."""
    h = get_current_hospital()

    if request.method == "PATCH":
        data = request.get_json(silent=True) or {}
        app_id = data.get("appointment_id")
        appt = Appointment.query.filter_by(id=app_id, hospital_id=h.id).first()
        if not appt:
            return jsonify({"success": False, "message": "Appointment not found"}), 404

        new_status = data.get("status")
        if new_status:
            appt.status = new_status
            db.session.commit()
            return jsonify({"success": True, "message": f"Appointment #{appt.id} status updated to {appt.status}"}), 200

    appointments = Appointment.query.filter_by(hospital_id=h.id).order_by(Appointment.appointment_date.desc()).all()
    appt_list = []
    for a in appointments:
        med_rec = MedicalRecord.query.filter_by(appointment_id=a.id).first()
        rx = Prescription.query.filter_by(medical_record_id=med_rec.id).first() if med_rec else None
        appt_list.append({
            "id": a.id,
            "patient_id": a.patient_id,
            "patient_name": a.patient.full_name if a.patient else "Patient",
            "doctor_id": a.doctor_id,
            "doctor_name": a.doctor.full_name if a.doctor else "Doctor",
            "doctor_specialization": a.doctor.specialization if a.doctor else "",
            "date": str(a.appointment_date),
            "time": str(a.appointment_time),
            "reason": a.reason,
            "status": a.status,
            "payment_status": a.payment_status,
            "has_prescription": rx is not None,
            "prescription": {
                "id": rx.id,
                "medicines": rx.medicines,
                "dosage": rx.dosage,
                "duration": rx.duration,
                "instructions": rx.instructions,
                "diagnosis": med_rec.diagnosis if med_rec else None,
                "follow_up_date": str(med_rec.follow_up_date) if (med_rec and med_rec.follow_up_date) else None
            } if rx else None
        })

    return jsonify({
        "success": True,
        "count": len(appt_list),
        "appointments": appt_list
    }), 200


@hospital_admin_bp.route("/appointments/<int:appt_id>/prescription", methods=["GET", "POST"])
@role_required("Hospital", "Admin")
def appointment_prescription(appt_id):
    """Issue or view digital prescription (e-Rx) for an OPD appointment."""
    h = get_current_hospital()
    appt = Appointment.query.filter_by(id=appt_id, hospital_id=h.id).first()
    if not appt:
        return jsonify({"success": False, "message": "Appointment not found in this facility"}), 404

    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        diagnosis = (data.get("diagnosis") or "").strip()
        medicines = (data.get("medicines") or "").strip()

        if not diagnosis or not medicines:
            return jsonify({"success": False, "message": "Diagnosis and medicines are required to issue an e-Rx"}), 400

        follow_up = None
        if data.get("follow_up_date"):
            try:
                follow_up = datetime.strptime(data.get("follow_up_date"), "%Y-%m-%d").date()
            except Exception:
                follow_up = None

        # Check if medical record already exists
        med_rec = MedicalRecord.query.filter_by(appointment_id=appt.id).first()
        if not med_rec:
            med_rec = MedicalRecord(
                patient_id=appt.patient_id,
                doctor_id=appt.doctor_id,
                appointment_id=appt.id,
                diagnosis=diagnosis,
                symptoms=data.get("symptoms", appt.reason or "General OPD Visit"),
                prescription=medicines,
                lab_tests=data.get("lab_tests", ""),
                notes=data.get("notes", ""),
                follow_up_date=follow_up
            )
            db.session.add(med_rec)
            db.session.flush()
        else:
            med_rec.diagnosis = diagnosis
            med_rec.symptoms = data.get("symptoms", med_rec.symptoms)
            med_rec.prescription = medicines
            med_rec.lab_tests = data.get("lab_tests", med_rec.lab_tests)
            med_rec.notes = data.get("notes", med_rec.notes)
            if follow_up:
                med_rec.follow_up_date = follow_up

        # Create or update prescription
        rx = Prescription.query.filter_by(medical_record_id=med_rec.id).first()
        if not rx:
            rx = Prescription(
                medical_record_id=med_rec.id,
                patient_id=appt.patient_id,
                doctor_id=appt.doctor_id,
                medicines=medicines,
                dosage=data.get("dosage", "1-0-1 (Morning & Night)"),
                duration=data.get("duration", "5 Days"),
                instructions=data.get("instructions", "Take after meals with warm water")
            )
            db.session.add(rx)
        else:
            rx.medicines = medicines
            rx.dosage = data.get("dosage", rx.dosage)
            rx.duration = data.get("duration", rx.duration)
            rx.instructions = data.get("instructions", rx.instructions)

        # Mark appointment completed
        appt.status = "Completed"
        db.session.commit()

        return jsonify({
            "success": True,
            "message": f"Digital Prescription (e-Rx) successfully issued for {appt.patient.full_name if appt.patient else 'Patient'}! It is now instantly available on their Patient Portal.",
            "prescription": {
                "id": rx.id,
                "medicines": rx.medicines,
                "dosage": rx.dosage,
                "duration": rx.duration,
                "instructions": rx.instructions,
                "diagnosis": med_rec.diagnosis,
                "follow_up_date": str(med_rec.follow_up_date) if med_rec.follow_up_date else None
            }
        }), 201

    # GET
    med_rec = MedicalRecord.query.filter_by(appointment_id=appt.id).first()
    rx = Prescription.query.filter_by(medical_record_id=med_rec.id).first() if med_rec else None
    if not rx:
        return jsonify({"success": True, "has_prescription": False, "prescription": None}), 200

    return jsonify({
        "success": True,
        "has_prescription": True,
        "prescription": {
            "id": rx.id,
            "medicines": rx.medicines,
            "dosage": rx.dosage,
            "duration": rx.duration,
            "instructions": rx.instructions,
            "diagnosis": med_rec.diagnosis if med_rec else None,
            "symptoms": med_rec.symptoms if med_rec else None,
            "lab_tests": med_rec.lab_tests if med_rec else None,
            "notes": med_rec.notes if med_rec else None,
            "follow_up_date": str(med_rec.follow_up_date) if (med_rec and med_rec.follow_up_date) else None
        }
    }), 200


@hospital_admin_bp.route("/beds", methods=["POST"])
@role_required("Hospital", "Admin")
def add_bed():
    """Register a new bed in this hospital."""
    h = get_current_hospital()
    data = request.get_json(silent=True) or {}
    bed_number = data.get("bed_number")
    ward = data.get("ward", "General Ward")
    bed_type = data.get("bed_type", "General")
    floor = data.get("floor", "1st Floor")
    room_number = data.get("room_number", "")
    notes = data.get("notes", "")

    if not bed_number:
        return jsonify({"success": False, "message": "Bed number is required"}), 400

    existing = Bed.query.filter_by(hospital_id=h.id, bed_number=bed_number).first()
    if existing:
        return jsonify({"success": False, "message": f"Bed '{bed_number}' already exists in this facility"}), 400

    bed = Bed(
        hospital_id=h.id,
        bed_number=bed_number,
        ward=ward,
        bed_type=bed_type,
        floor=floor,
        room_number=room_number,
        status="Available",
        notes=notes
    )
    db.session.add(bed)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"{bed_type} Bed {bed_number} registered successfully!",
        "bed": {
            "id": bed.id,
            "bed_number": bed.bed_number,
            "ward": bed.ward,
            "bed_type": bed.bed_type,
            "floor": bed.floor,
            "room_number": bed.room_number,
            "status": bed.status,
            "notes": bed.notes
        }
    }), 201


@hospital_admin_bp.route("/beds/<int:bed_id>", methods=["DELETE"])
@role_required("Hospital", "Admin")
def delete_bed(bed_id):
    """Remove a bed from inventory."""
    h = get_current_hospital()
    bed = Bed.query.filter_by(id=bed_id, hospital_id=h.id).first()
    if not bed:
        return jsonify({"success": False, "message": "Bed not found"}), 404

    db.session.delete(bed)
    db.session.commit()
    return jsonify({"success": True, "message": f"Bed {bed.bed_number} removed from inventory"}), 200


@hospital_admin_bp.route("/ambulances", methods=["POST"])
@role_required("Hospital", "Admin")
def add_ambulance():
    """Register a new emergency ambulance unit."""
    h = get_current_hospital()
    data = request.get_json(silent=True) or {}
    reg_no = data.get("registration_number")
    amb_type = data.get("ambulance_type", "Advanced Life Support (ALS)")
    driver_name = data.get("driver_name", "Paramedic Driver")
    driver_phone = data.get("driver_phone", "+91 9800001080")
    location = data.get("current_location", f"{h.name}, {h.city}")

    if not reg_no:
        return jsonify({"success": False, "message": "Registration number is required"}), 400

    amb = Ambulance(
        hospital_id=h.id,
        registration_number=reg_no,
        ambulance_type=amb_type,
        driver_name=driver_name,
        driver_phone=driver_phone,
        current_location=location,
        availability_status="Available"
    )
    db.session.add(amb)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Ambulance {reg_no} registered successfully!",
        "ambulance": {
            "id": amb.id,
            "registration_number": amb.registration_number,
            "ambulance_type": amb.ambulance_type,
            "driver_name": amb.driver_name,
            "driver_phone": amb.driver_phone,
            "current_location": amb.current_location,
            "availability_status": amb.availability_status
        }
    }), 201


@hospital_admin_bp.route("/doctors", methods=["GET"])
@role_required("Hospital", "Admin")
def list_doctors():
    """List specialist doctors on duty for this facility."""
    h = get_current_hospital()
    doctors = Doctor.query.filter_by(hospital_id=h.id).all()
    return jsonify({
        "success": True,
        "count": len(doctors),
        "doctors": [
            {
                "id": d.id,
                "full_name": d.full_name,
                "email": d.email,
                "phone": d.phone or "+91 9830000000",
                "specialization": d.specialization,
                "qualification": d.qualification or "MBBS, MD",
                "experience": d.experience or 5,
                "consultation_fee": d.consultation_fee or 800,
                "is_active": d.is_active,
                "schedules_count": len(d.schedules) if d.schedules else 0
            } for d in doctors
        ]
    }), 200


@hospital_admin_bp.route("/doctors", methods=["POST"])
@role_required("Hospital", "Admin")
def add_doctor():
    """Add a new doctor to the hospital roster."""
    h = get_current_hospital()
    data = request.get_json(silent=True) or {}
    full_name = data.get("full_name")
    email = data.get("email")
    phone = data.get("phone", "+91 9800000000")
    specialization = data.get("specialization", "General Medicine")
    qualification = data.get("qualification", "MBBS, MD")
    experience = data.get("experience", 5)
    fee = data.get("consultation_fee", 800)

    if not full_name or not email:
        return jsonify({"success": False, "message": "Doctor full name and email are required"}), 400

    existing = Doctor.query.filter_by(email=email).first()
    if existing:
        return jsonify({"success": False, "message": f"Doctor with email {email} already registered"}), 400

    doctor = Doctor(
        hospital_id=h.id,
        full_name=full_name,
        email=email,
        phone=phone,
        specialization=specialization,
        qualification=qualification,
        experience=int(experience),
        consultation_fee=float(fee),
        is_active=True
    )
    db.session.add(doctor)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Dr. {full_name} added to hospital roster!",
        "doctor": {
            "id": doctor.id,
            "full_name": doctor.full_name,
            "specialization": doctor.specialization,
            "consultation_fee": doctor.consultation_fee,
            "is_active": doctor.is_active
        }
    }), 201


@hospital_admin_bp.route("/doctors/<int:doc_id>", methods=["PATCH"])
@role_required("Hospital", "Admin")
def update_doctor(doc_id):
    """Toggle doctor availability or update fees."""
    h = get_current_hospital()
    doc = Doctor.query.filter_by(id=doc_id, hospital_id=h.id).first()
    if not doc:
        return jsonify({"success": False, "message": "Doctor not found in this facility"}), 404

    data = request.get_json(silent=True) or {}
    if "is_active" in data:
        doc.is_active = bool(data["is_active"])
    if "consultation_fee" in data:
        doc.consultation_fee = float(data["consultation_fee"])
    if "phone" in data:
        doc.phone = data["phone"]

    db.session.commit()
    return jsonify({
        "success": True,
        "message": f"Dr. {doc.full_name} profile updated",
        "doctor": {
            "id": doc.id,
            "full_name": doc.full_name,
            "is_active": doc.is_active,
            "consultation_fee": doc.consultation_fee
        }
    }), 200


@hospital_admin_bp.route("/info", methods=["PUT"])
@role_required("Hospital", "Admin")
def update_hospital_info():
    """Update facility contact and operation details."""
    h = get_current_hospital()
    data = request.get_json(silent=True) or {}

    if "name" in data and data["name"]:
        h.name = data["name"].strip()
    if "phone" in data:
        h.phone = data["phone"].strip()
    if "emergency_contact" in data:
        h.emergency_contact = data["emergency_contact"].strip()
    if "city" in data:
        h.city = data["city"].strip()
    if "address" in data:
        h.address = data["address"].strip()

    db.session.commit()
    return jsonify({
        "success": True,
        "message": f"{h.name} facility details updated successfully!",
        "hospital": {
            "id": h.id,
            "name": h.name,
            "city": h.city,
            "phone": h.phone,
            "emergency_contact": h.emergency_contact
        }
    }), 200
