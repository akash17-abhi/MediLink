def validate_prescription(data):

    required_fields = [
        "medical_record_id",
        "patient_id",
        "doctor_id",
        "medicines"
    ]

    for field in required_fields:
        if field not in data or data[field] in (None, ""):
            return False, f"{field} is required"

    return True, ""


def prescription_to_dict(prescription):

    return {
        "id": prescription.id,
        "medical_record_id": prescription.medical_record_id,
        "patient_id": prescription.patient_id,
        "doctor_id": prescription.doctor_id,
        "medicines": prescription.medicines,
        "dosage": prescription.dosage,
        "duration": prescription.duration,
        "instructions": prescription.instructions,
        "created_at": prescription.created_at.strftime("%Y-%m-%d %H:%M:%S")
        if prescription.created_at else None,
        "updated_at": prescription.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        if prescription.updated_at else None
    }