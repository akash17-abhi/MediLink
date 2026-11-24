"""
Role and permission definitions for MediLink platform.
"""

class Roles:
    ADMIN = "Admin"
    HOSPITAL = "Hospital"
    DOCTOR = "Doctor"
    PATIENT = "Patient"
    AMBULANCE = "Ambulance Owner"
    LABORATORY = "Laboratory"

    ALL_ROLES = [
        ADMIN,
        HOSPITAL,
        DOCTOR,
        PATIENT,
        AMBULANCE,
        LABORATORY
    ]


class Permissions:
    # Patient permissions
    BOOK_APPOINTMENT = "book_appointment"
    REQUEST_EMERGENCY = "request_emergency"
    VIEW_OWN_RECORDS = "view_own_records"

    # Hospital Admin permissions
    MANAGE_HOSPITAL_BEDS = "manage_hospital_beds"
    MANAGE_HOSPITAL_AMBULANCES = "manage_hospital_ambulances"
    HANDLE_EMERGENCIES = "handle_emergencies"
    MANAGE_DOCTORS = "manage_doctors"

    # Super Admin permissions
    MANAGE_ALL_USERS = "manage_all_users"
    MANAGE_ALL_HOSPITALS = "manage_all_hospitals"
    VIEW_ANALYTICS = "view_analytics"
    SYSTEM_CONFIG = "system_config"


def has_role(user, *role_names):
    """Check if the given user object has any of the specified roles."""
    if not user or not hasattr(user, "roles"):
        return False
    user_roles = {r.name for r in user.roles}
    return any(r in user_roles for r in role_names)
