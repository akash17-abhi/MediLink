# backend/app/repositories/__init__.py

from .base_repository import BaseRepository
from .hospital_repository import HospitalRepository
from .doctor_repository import DoctorRepository
from .patient_repository import PatientRepository  # Add this
from .medical_record_repository import MedicalRecordRepository
from .notification_repository import NotificationRepository
__all__ = [
    'BaseRepository',
    'HospitalRepository',
    'DoctorRepository',
    'PatientRepository',
    'MedicalRecordRepository',
    'NotificationRepository',  # Add this
]