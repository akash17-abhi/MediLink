# backend/app/schemas/__init__.py

from .auth_schema import *
from .hospital_schema import *
from .doctor_schema import *
from .patient_schema import *

from .notification_schema import (
    validate_notification,
    notification_to_dict
)

# =========================================================
# BED MANAGEMENT
# =========================================================

from .bed_schema import (
    BedCreateSchema,
    BedUpdateSchema,
    BedStatusSchema,
    BedAssignPatientSchema,
    BedResponseSchema,
)


# =========================================================
# EXPORTED SCHEMAS / FUNCTIONS
# =========================================================

__all__ = [
    "auth_schema",
    "hospital_schema",
    "doctor_schema",
    "patient_schema",

    "validate_notification",
    "notification_to_dict",

    "BedCreateSchema",
    "BedUpdateSchema",
    "BedStatusSchema",
    "BedAssignPatientSchema",
    "BedResponseSchema",
]