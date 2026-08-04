from app.models.doctor import Doctor
from app.repositories.doctor_repository import DoctorRepository


class DoctorService:

    @staticmethod
    def create(data):

        existing = DoctorRepository.get_by_email(data["email"])

        if existing:
            return None, "Doctor email already exists"

        doctor = Doctor(
            full_name=data["full_name"],
            email=data["email"],
            phone=data.get("phone"),
            specialization=data["specialization"],
            qualification=data.get("qualification"),
            experience=data.get("experience", 0),
            consultation_fee=data.get("consultation_fee", 0),
            profile_photo=data.get("profile_photo"),
            hospital_id=data["hospital_id"]
        )

        DoctorRepository.create(doctor)

        return doctor, None

    @staticmethod
    def get_all():
        return DoctorRepository.get_all()

    @staticmethod
    def get_by_id(doctor_id):
        return DoctorRepository.get_by_id(doctor_id)

    @staticmethod
    def update(doctor_id, data):

        doctor = DoctorRepository.get_by_id(doctor_id)

        if not doctor:
            return None

        for key, value in data.items():
            setattr(doctor, key, value)

        DoctorRepository.update()

        return doctor

    @staticmethod
    def delete(doctor_id):

        doctor = DoctorRepository.get_by_id(doctor_id)

        if not doctor:
            return False

        DoctorRepository.delete(doctor)

        return True