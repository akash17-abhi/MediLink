def validate_doctor(data):

    required_fields = [
        "hospital_id",
        "full_name",
        "email",
        "phone",
        "specialization"
    ]

    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"{field} is required"

    return True, ""


def doctor_to_dict(doctor):

    return {
        "id": doctor.id,
        "full_name": doctor.full_name,
        "email": doctor.email,
        "phone": doctor.phone,
        "specialization": doctor.specialization,
        "qualification": doctor.qualification,
        "experience": doctor.experience,
        "consultation_fee": doctor.consultation_fee,
        "profile_photo": doctor.profile_photo,
        "hospital_id": doctor.hospital_id,
        "is_active": doctor.is_active,
        "created_at": doctor.created_at,
        "updated_at": doctor.updated_at
    }