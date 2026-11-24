from app.models.bill import Bill

from app.repositories.bill_repository import BillRepository
from app.repositories.patient_repository import PatientRepository
from app.repositories.doctor_repository import DoctorRepository
from app.repositories.hospital_repository import HospitalRepository


class BillService:

    # =====================================================
    # CREATE BILL
    # =====================================================

    @staticmethod
    def create(data):

        # -------------------------------------------------
        # Check patient
        # -------------------------------------------------

        patient = PatientRepository().get_by_id(
            data["patient_id"]
        )

        if not patient:
            return None, "Patient not found"

        # -------------------------------------------------
        # Check doctor
        # -------------------------------------------------

        doctor = DoctorRepository.get_by_id(
            data["doctor_id"]
        )

        if not doctor:
            return None, "Doctor not found"

        # -------------------------------------------------
        # Check hospital
        # -------------------------------------------------

        hospital = HospitalRepository.get_by_id(
            data["hospital_id"]
        )

        if not hospital:
            return None, "Hospital not found"

        # -------------------------------------------------
        # Convert charges safely
        # -------------------------------------------------

        consultation_charge = float(
            data.get("consultation_charge", 0)
        )

        laboratory_charge = float(
            data.get("laboratory_charge", 0)
        )

        medicine_charge = float(
            data.get("medicine_charge", 0)
        )

        other_charge = float(
            data.get("other_charge", 0)
        )

        discount = float(
            data.get("discount", 0)
        )

        tax = float(
            data.get("tax", 0)
        )

        # -------------------------------------------------
        # Calculate total
        # -------------------------------------------------

        total_amount = (
            consultation_charge
            + laboratory_charge
            + medicine_charge
            + other_charge
            - discount
            + tax
        )

        # -------------------------------------------------
        # Prevent negative bill
        # -------------------------------------------------

        if total_amount < 0:
            return None, "Total bill amount cannot be negative"

        # -------------------------------------------------
        # Create bill
        # -------------------------------------------------

        bill = Bill(

            patient_id=data["patient_id"],

            doctor_id=data["doctor_id"],

            hospital_id=data["hospital_id"],

            consultation_charge=consultation_charge,

            laboratory_charge=laboratory_charge,

            medicine_charge=medicine_charge,

            other_charge=other_charge,

            discount=discount,

            tax=tax,

            total_amount=total_amount,

            payment_status=data.get(
                "payment_status",
                "Pending"
            )
        )

        # -------------------------------------------------
        # Save
        # -------------------------------------------------

        BillRepository.create(bill)

        return bill, None

    # =====================================================
    # GET ALL BILLS
    # =====================================================

    @staticmethod
    def get_all():

        return BillRepository.get_all()

    # =====================================================
    # GET BILL BY ID
    # =====================================================

    @staticmethod
    def get_by_id(bill_id):

        return BillRepository.get_by_id(
            bill_id
        )

    # =====================================================
    # UPDATE BILL
    # =====================================================

    @staticmethod
    def update(bill_id, data):

        bill = BillRepository.get_by_id(
            bill_id
        )

        if not bill:
            return None, "Bill not found"

        # -------------------------------------------------
        # Protected fields
        # -------------------------------------------------

        protected_fields = {
            "id",
            "created_at",
            "updated_at",
            "total_amount"
        }

        # -------------------------------------------------
        # Allowed fields
        # -------------------------------------------------

        allowed_fields = {
            "patient_id",
            "doctor_id",
            "hospital_id",
            "consultation_charge",
            "laboratory_charge",
            "medicine_charge",
            "other_charge",
            "discount",
            "tax",
            "payment_status"
        }

        # -------------------------------------------------
        # Validate patient
        # -------------------------------------------------

        if "patient_id" in data:

            patient = PatientRepository().get_by_id(
                data["patient_id"]
            )

            if not patient:
                return None, "Patient not found"

        # -------------------------------------------------
        # Validate doctor
        # -------------------------------------------------

        if "doctor_id" in data:

            doctor = DoctorRepository.get_by_id(
                data["doctor_id"]
            )

            if not doctor:
                return None, "Doctor not found"

        # -------------------------------------------------
        # Validate hospital
        # -------------------------------------------------

        if "hospital_id" in data:

            hospital = HospitalRepository.get_by_id(
                data["hospital_id"]
            )

            if not hospital:
                return None, "Hospital not found"

        # -------------------------------------------------
        # Numeric fields
        # -------------------------------------------------

        numeric_fields = {
            "consultation_charge",
            "laboratory_charge",
            "medicine_charge",
            "other_charge",
            "discount",
            "tax"
        }

        # -------------------------------------------------
        # Update fields
        # -------------------------------------------------

        for key, value in data.items():

            if key in protected_fields:
                continue

            if key not in allowed_fields:
                continue

            if key in numeric_fields:

                try:
                    value = float(value)

                except (ValueError, TypeError):

                    return (
                        None,
                        f"{key} must be a valid number"
                    )

                if value < 0:

                    return (
                        None,
                        f"{key} cannot be negative"
                    )

            setattr(
                bill,
                key,
                value
            )

        # -------------------------------------------------
        # Recalculate total
        # -------------------------------------------------

        bill.total_amount = (

            float(
                bill.consultation_charge or 0
            )

            + float(
                bill.laboratory_charge or 0
            )

            + float(
                bill.medicine_charge or 0
            )

            + float(
                bill.other_charge or 0
            )

            - float(
                bill.discount or 0
            )

            + float(
                bill.tax or 0
            )
        )

        # -------------------------------------------------
        # Prevent negative total
        # -------------------------------------------------

        if bill.total_amount < 0:

            return (
                None,
                "Total bill amount cannot be negative"
            )

        # -------------------------------------------------
        # Save
        # -------------------------------------------------

        BillRepository.update()

        return bill, None

    # =====================================================
    # DELETE BILL
    # =====================================================

    @staticmethod
    def delete(bill_id):

        bill = BillRepository.get_by_id(
            bill_id
        )

        if not bill:
            return False

        BillRepository.delete(
            bill
        )

        return True

    # =====================================================
    # GET PATIENT BILLS
    # =====================================================

    @staticmethod
    def get_by_patient(patient_id):

        return BillRepository.get_by_patient(
            patient_id
        )