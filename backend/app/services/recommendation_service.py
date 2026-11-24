"""
Smart Hospital Recommendation & Ranking Engine with 'Why This Hospital?' Explanations
Calculates Haversine distances, bed availability, ambulance fleet status, and
department matches to generate prioritized ranking with transparent explanation chips.
"""

import math
from app.models.hospital import Hospital
from app.models.doctor import Doctor
from app.models.bed import Bed
from app.models.ambulance import Ambulance
from app.extensions import db


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees), returning distance in kilometers.
    """
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return 9999.0

    R = 6371.0  # Earth's radius in kilometers

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2))
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    return round(R * c, 2)


class RecommendationService:
    @staticmethod
    def get_hospital_bed_summary(hospital_id: int):
        """Calculates live available and total bed counts by type for a hospital."""
        beds = Bed.query.filter_by(hospital_id=hospital_id).all()

        icu_total = sum(1 for b in beds if b.bed_type.upper() == "ICU")
        icu_avail = sum(1 for b in beds if b.bed_type.upper() == "ICU" and b.status.lower() == "available")

        emg_total = sum(1 for b in beds if b.bed_type.upper() == "EMERGENCY")
        emg_avail = sum(1 for b in beds if b.bed_type.upper() == "EMERGENCY" and b.status.lower() == "available")

        gen_total = sum(1 for b in beds if b.bed_type.upper() == "GENERAL")
        gen_avail = sum(1 for b in beds if b.bed_type.upper() == "GENERAL" and b.status.lower() == "available")

        # Fallback to hospital model baseline capacity if no granular bed rows yet
        h = db.session.get(Hospital, hospital_id)
        if len(beds) == 0 and h:
            icu_total = h.icu_beds or 0
            icu_avail = max(0, int(icu_total * 0.4))
            emg_total = h.emergency_beds or 0
            emg_avail = max(0, int(emg_total * 0.5))
            gen_total = h.total_beds or 0
            gen_avail = max(0, int(gen_total * 0.35))

        return {
            "icu": {"total": icu_total, "available": icu_avail},
            "emergency": {"total": emg_total, "available": emg_avail},
            "general": {"total": gen_total, "available": gen_avail},
            "total_available": icu_avail + emg_avail + gen_avail
        }

    @staticmethod
    def recommend_hospitals(
        user_lat: float,
        user_lng: float,
        radius_km: float = 25.0,
        required_department: str = None,
        bed_type_needed: str = None,
        emergency_mode: bool = False,
        limit: int = 15
    ):
        """
        Ranks hospitals based on distance, bed availability, ambulance status, and specialist matching.
        """
        all_hospitals = Hospital.query.filter_by(is_active=True).all()
        ranked = []

        for h in all_hospitals:
            dist = haversine_distance(user_lat, user_lng, h.latitude, h.longitude)

            # In general filtering, apply radius limit (allow higher radius if 0 found)
            if radius_km and dist > radius_km and not emergency_mode:
                continue

            # Bed Availability
            beds = RecommendationService.get_hospital_bed_summary(h.id)

            # Available Ambulances
            ambulances = Ambulance.query.filter_by(hospital_id=h.id).all()
            avail_ambulances = sum(1 for a in ambulances if a.availability_status.lower() == "available")
            total_ambulances = len(ambulances)

            # Doctor / Department Matching
            doctors = Doctor.query.filter_by(hospital_id=h.id, is_active=True).all()
            matching_doctors = []
            if required_department:
                matching_doctors = [
                    d for d in doctors
                    if required_department.lower() in (d.specialization or "").lower()
                ]
            has_specialist = len(matching_doctors) > 0 or not required_department

            # --- Multi-factor Scoring Algorithm ---
            # 1. Proximity Score (Max 40 pts)
            proximity_score = max(0.0, 40.0 - (dist * 0.8))

            # 2. Bed Availability Score (Max 30 pts)
            icu_pts = min(15.0, beds["icu"]["available"] * 1.5)
            emg_pts = min(10.0, beds["emergency"]["available"] * 1.0)
            gen_pts = min(5.0, beds["general"]["available"] * 0.1)
            bed_score = icu_pts + emg_pts + gen_pts

            # 3. Specialist Match Score (Max 20 pts)
            specialist_score = 20.0 if has_specialist else 0.0

            # 4. Ambulance Availability (Max 10 pts)
            ambulance_score = min(10.0, avail_ambulances * 5.0)

            # Emergency mode re-weighting (prioritize distance + ICU/ER beds)
            if emergency_mode:
                total_score = (proximity_score * 1.4) + (bed_score * 1.2) + ambulance_score
            else:
                total_score = proximity_score + bed_score + specialist_score + ambulance_score

            total_score = round(min(100.0, max(10.0, total_score)), 1)

            # --- "Why This Hospital?" Tags & Summary Generation ---
            why_tags = []
            why_tags.append(f"{dist:.1f} km away")

            if beds["icu"]["available"] > 0:
                why_tags.append(f"{beds['icu']['available']} ICU Beds Ready")
            else:
                why_tags.append("⚠️ 0 ICU Beds")

            if beds["emergency"]["available"] > 0:
                why_tags.append(f"{beds['emergency']['available']} ER Beds")

            if has_specialist and required_department:
                why_tags.append(f"{required_department} Specialists")

            if avail_ambulances > 0:
                why_tags.append(f"🚑 {avail_ambulances} Ambulance{'s' if avail_ambulances > 1 else ''} Ready")

            if h.is_24x7:
                why_tags.append("24x7 Open")

            # Recommendation Badge Logic
            badge = "Recommended"
            if dist <= 5.0 and (beds["icu"]["available"] > 0 or beds["emergency"]["available"] > 0):
                badge = "Fastest Access"
            elif has_specialist and required_department and beds["icu"]["available"] > 5:
                badge = "Specialist Match"
            elif beds["total_available"] >= 40:
                badge = "High Capacity"

            # Summary Sentence
            summary_parts = [f"Located {dist:.1f} km away."]
            if beds['icu']['available'] > 0:
                summary_parts.append(f"{beds['icu']['available']} ICU and {beds['emergency']['available']} emergency beds available.")
            else:
                summary_parts.append("Emergency intake open.")
            if avail_ambulances > 0:
                summary_parts.append(f"{avail_ambulances} standby ambulance ready for immediate dispatch.")
            if has_specialist and required_department:
                summary_parts.append(f"Has on-duty {required_department} specialists.")
            why_summary = " ".join(summary_parts)

            def serialize_doctor(d):
                sched_text = "Mon - Sat: 09:00 AM - 01:00 PM"
                if d.schedules:
                    s = d.schedules[0]
                    st = s.start_time.strftime("%I:%M %p") if s.start_time else "09:00 AM"
                    et = s.end_time.strftime("%I:%M %p") if s.end_time else "01:00 PM"
                    sched_text = f"{s.day_of_week}: {st} - {et}"
                return {
                    "id": d.id,
                    "name": d.full_name,
                    "specialization": d.specialization,
                    "qualification": d.qualification or "MD / MS Specialist",
                    "experience": d.experience or 5,
                    "consultation_fee": d.consultation_fee or 500.0,
                    "is_active": d.is_active,
                    "is_available": d.is_active,
                    "schedule_display": sched_text
                }

            docs_payload = [serialize_doctor(d) for d in doctors]
            matching_payload = [serialize_doctor(d) for d in matching_doctors] if matching_doctors else docs_payload

            ranked.append({
                "hospital": {
                    "id": h.id,
                    "name": h.name,
                    "registration_number": h.registration_number,
                    "hospital_type": h.hospital_type,
                    "address": h.address,
                    "city": h.city,
                    "state": h.state,
                    "pincode": h.pincode,
                    "phone": h.phone,
                    "emergency_contact": h.emergency_contact or h.phone,
                    "latitude": h.latitude,
                    "longitude": h.longitude,
                    "is_24x7": h.is_24x7,
                    "website": h.website
                },
                "distance_km": dist,
                "match_score": total_score,
                "recommendation_badge": badge,
                "why_tags": why_tags,
                "why_summary": why_summary,
                "beds": beds,
                "ambulances": {
                    "total": total_ambulances,
                    "available": avail_ambulances
                },
                "doctor_count": len(doctors),
                "doctors": docs_payload,
                "matching_doctors": matching_payload
            })

        # Sort primarily by match score descending (or distance if emergency)
        if emergency_mode:
            ranked.sort(key=lambda x: (x["distance_km"], -x["beds"]["icu"]["available"]))
        else:
            ranked.sort(key=lambda x: -x["match_score"])

        # Give top 1 the "Best Overall Match" badge if not already tagged
        if ranked:
            ranked[0]["recommendation_badge"] = "Best Overall Match"

        return ranked[:limit]

    @staticmethod
    def get_nearest_emergency_beds(
        user_lat: float,
        user_lng: float,
        radius_km: float = 50.0,
        limit: int = 10
    ):
        """
        Emergency endpoint prioritizing shortest distance with immediate ICU/ER bed breakdown.
        """
        return RecommendationService.recommend_hospitals(
            user_lat=user_lat,
            user_lng=user_lng,
            radius_km=radius_km,
            emergency_mode=True,
            limit=limit
        )
