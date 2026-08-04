def validate_register(data):

    required_fields = [
        "full_name",
        "email",
        "password"
    ]

    for field in required_fields:

        if field not in data or not data[field]:

            return False, f"{field} is required"

    return True, ""


def validate_login(data):

    required_fields = [
        "email",
        "password"
    ]

    for field in required_fields:

        if field not in data or not data[field]:

            return False, f"{field} is required"

    return True, ""