"""
Recommendation & Emergency Search API Endpoints
Provides:
  - POST /api/recommend/department : AIML Symptom Classifier
  - GET/POST /api/hospitals/recommend : Smart Hospital Ranker + 'Why This Hospital?'
  - GET /api/emergencies/nearest-beds : Fast ICU/Emergency bed locator
  - GET /api/specializations : All clinical departments
"""

from flask import Blueprint, request, jsonify
from app.services.symptom_service import SymptomService
from app.services.recommendation_service import RecommendationService
from app.models.specialization import Specialization
from app.models.doctor import Doctor

recommend_bp = Blueprint("recommendations", __name__, url_prefix="/api")


@recommend_bp.route("/recommend/department", methods=["GET", "POST"])
def recommend_department():
    """Classify free-text symptoms into recommended medical department."""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        symptoms = data.get("symptoms", "")
    else:
        symptoms = request.args.get("symptoms", "")

    result = SymptomService.classify_symptoms(symptoms)
    return jsonify({
        "success": True,
        "data": result
    }), 200


@recommend_bp.route("/hospitals/recommend", methods=["GET", "POST"])
def recommend_hospitals():
    """Rank nearby hospitals with distance, beds, ambulance, and 'Why This Hospital?' tags."""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        lat = float(data.get("lat") or 22.5726)
        lng = float(data.get("lng") or 88.3639)
        radius = float(data.get("radius_km") or 25.0)
        dept = data.get("department") or data.get("specialization")
        bed_type = data.get("bed_type")
        emergency_mode = bool(data.get("emergency_mode", False))
        limit = int(data.get("limit") or 15)
    else:
        lat = float(request.args.get("lat", 22.5726))
        lng = float(request.args.get("lng", 88.3639))
        radius = float(request.args.get("radius_km", 25.0))
        dept = request.args.get("department") or request.args.get("specialization")
        bed_type = request.args.get("bed_type")
        emergency_mode = request.args.get("emergency_mode", "false").lower() == "true"
        limit = int(request.args.get("limit", 15))

    results = RecommendationService.recommend_hospitals(
        user_lat=lat,
        user_lng=lng,
        radius_km=radius,
        required_department=dept,
        bed_type_needed=bed_type,
        emergency_mode=emergency_mode,
        limit=limit
    )

    return jsonify({
        "success": True,
        "count": len(results),
        "data": results,
        "query": {
            "lat": lat,
            "lng": lng,
            "radius_km": radius,
            "department": dept,
            "emergency_mode": emergency_mode
        }
    }), 200


@recommend_bp.route("/emergencies/nearest-beds", methods=["GET"])
def nearest_emergency_beds():
    """Returns nearest hospitals with immediate ICU/Emergency/General bed availability."""
    lat = float(request.args.get("lat", 22.5726))
    lng = float(request.args.get("lng", 88.3639))
    radius = float(request.args.get("radius_km", 50.0))
    limit = int(request.args.get("limit", 10))

    results = RecommendationService.get_nearest_emergency_beds(
        user_lat=lat,
        user_lng=lng,
        radius_km=radius,
        limit=limit
    )

    return jsonify({
        "success": True,
        "count": len(results),
        "emergency_alert": "Critical Triage Active",
        "data": results
    }), 200


@recommend_bp.route("/specializations", methods=["GET"])
def get_specializations():
    """List all clinical medical departments."""
    specs = Specialization.query.filter_by(is_active=True).all()
    return jsonify({
        "success": True,
        "count": len(specs),
        "data": [s.to_dict() for s in specs]
    }), 200


@recommend_bp.route("/hospitals/<int:hospital_id>/doctors", methods=["GET"])
def get_hospital_doctors(hospital_id):
    """Retrieve all active doctors with consultation fees and schedules for a hospital."""
    doctors = Doctor.query.filter_by(hospital_id=hospital_id, is_active=True).all()
    result = []
    for d in doctors:
        sched_text = "Mon - Sat: 09:00 AM - 01:00 PM"
        if d.schedules:
            s = d.schedules[0]
            st = s.start_time.strftime("%I:%M %p") if s.start_time else "09:00 AM"
            et = s.end_time.strftime("%I:%M %p") if s.end_time else "01:00 PM"
            sched_text = f"{s.day_of_week}: {st} - {et}"
        result.append({
            "id": d.id,
            "name": d.full_name,
            "specialization": d.specialization,
            "qualification": d.qualification or "MD / MS Specialist",
            "experience": d.experience or 5,
            "consultation_fee": d.consultation_fee or 500.0,
            "is_active": d.is_active,
            "is_available": d.is_active,
            "schedule_display": sched_text
        })
    return jsonify({
        "success": True,
        "hospital_id": hospital_id,
        "count": len(result),
        "doctors": result
    }), 200
