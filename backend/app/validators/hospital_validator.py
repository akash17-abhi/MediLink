def validate_hospital(data):

    required_fields = [
        "name",
        "registration_number",
        "hospital_type",
        "email",
        "phone",
        "address",
        "city",
        "state",
        "pincode"
    ]

    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"{field} is required"

    return True, ""