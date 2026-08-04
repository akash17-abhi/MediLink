def validate_register(data):

    required_fields = [
        "full_name",
        "email",
        "password"
    ]

    for field in required_fields:

        if field not in data:

            return False, f"{field} is required"

    return True, ""