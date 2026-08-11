from app.models.bill import Bill

from app.repositories.bill_repository import BillRepository
from app.repositories.patient_repository import PatientRepository
from app.repositories.doctor_repository import DoctorRepository
from app.repositories.hospital_repository import HospitalRepository


class BillService:

    @staticmethod
    def create(data):

        patient = PatientRepository().get_by_id(
            data["patient_id"]
        )

        if not patient:
            return None, "Patient not found"

        doctor = DoctorRepository.get_by_id(
            data["doctor_id"]
        )

        if not doctor:
            return None, "Doctor not found"

        hospital = HospitalRepository.get_by_id(
            data["hospital_id"]
        )

        if not hospital:
            return None, "Hospital not found"

        subtotal = (
            float(data.get("consultation_charge", 0))
            + float(data.get("laboratory_charge", 0))
            + float(data.get("medicine_charge", 0))
            + float(data.get("other_charge", 0))
        )

        subtotal -= float(data.get("discount", 0))
        subtotal += float(data.get("tax", 0))

        bill = Bill(
            patient_id=data["patient_id"],
            doctor_id=data["doctor_id"],
            hospital_id=data["hospital_id"],
            consultation_charge=data.get("consultation_charge", 0),
            laboratory_charge=data.get("laboratory_charge", 0),
            medicine_charge=data.get("medicine_charge", 0),
            other_charge=data.get("other_charge", 0),
            discount=data.get("discount", 0),
            tax=data.get("tax", 0),
            total_amount=subtotal,
            payment_status=data.get("payment_status", "Pending")
        )

        BillRepository.create(bill)

        return bill, None

    @staticmethod
    def get_all():
        return BillRepository.get_all()

    @staticmethod
    def get_by_id(bill_id):
        return BillRepository.get_by_id(bill_id)

    @staticmethod
    def update(bill_id, data):

        bill = BillRepository.get_by_id(bill_id)

        if not bill:
            return None

        for key, value in data.items():
            setattr(bill, key, value)

        bill.total_amount = (
            bill.consultation_charge
            + bill.laboratory_charge
            + bill.medicine_charge
            + bill.other_charge
            - bill.discount
            + bill.tax
        )

        BillRepository.update()

        return bill

    @staticmethod
    def delete(bill_id):

        bill = BillRepository.get_by_id(bill_id)

        if not bill:
            return False

        BillRepository.delete(bill)

        return True

    @staticmethod
    def get_by_patient(patient_id):
        return BillRepository.get_by_patient(patient_id)