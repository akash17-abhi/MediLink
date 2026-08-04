from app.repositories.hospital_repository import HospitalRepository


class HospitalService:

    @staticmethod
    def create_hospital(data):

        if HospitalRepository.get_by_email(data["email"]):
            return None, "Hospital email already exists."

        if HospitalRepository.get_by_registration_number(
            data["registration_number"]
        ):
            return None, "Registration number already exists."

        hospital = HospitalRepository.create(data)

        return hospital, None

    @staticmethod
    def get_all_hospitals():
        return HospitalRepository.get_all()

    @staticmethod
    def get_hospital(hospital_id):
        return HospitalRepository.get_by_id(hospital_id)

    @staticmethod
    def update_hospital(hospital, data):
        return HospitalRepository.update(hospital, data)

    @staticmethod
    def delete_hospital(hospital):
        HospitalRepository.delete(hospital)