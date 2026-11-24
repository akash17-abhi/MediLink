# backend/app/services/__init__.py

from .auth_service import AuthService
from .hospital_service import HospitalService
from .doctor_service import DoctorService
from .patient_service import PatientService  # Add this
from .notification_service import NotificationService
from .bed_service import BedService
__all__ = [
    'AuthService',
    'HospitalService',
    'DoctorService',
    'PatientService',  # Add this
    'NotificationService',
    'BedService'  # Add this
]