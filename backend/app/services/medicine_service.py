from datetime import datetime

from app.models.medicine import Medicine

from app.repositories.medicine_repository import (
    MedicineRepository
)

from app.repositories.hospital_repository import (
    HospitalRepository
)


class MedicineService:

    # =====================================================
    # CREATE
    # =====================================================

    @staticmethod
    def create(data):

        # Check hospital
        hospital = HospitalRepository.get_by_id(
            data["hospital_id"]
        )

        if not hospital:
            return None, "Hospital not found"

        # Check duplicate medicine in same hospital
        existing = Medicine.query.filter_by(
            hospital_id=data["hospital_id"],
            name=data["name"]
        ).first()

        if existing:
            return None, "Medicine already exists in this hospital"

        # Convert expiry date
        expiry = None

        if data.get("expiry_date"):

            try:
                expiry = datetime.strptime(
                    data["expiry_date"],
                    "%Y-%m-%d"
                ).date()

            except ValueError:
                return None, "expiry_date must be YYYY-MM-DD"

        # Create medicine
        medicine = Medicine(
            hospital_id=data["hospital_id"],
            name=data["name"],
            generic_name=data.get("generic_name"),
            manufacturer=data.get("manufacturer"),
            category=data.get("category"),
            batch_number=data.get("batch_number"),
            expiry_date=expiry,
            price=data.get("price", 0),
            stock_quantity=data.get("stock_quantity", 0),
            minimum_stock=data.get("minimum_stock", 10),
            description=data.get("description"),
            is_active=data.get("is_active", True)
        )

        MedicineRepository.create(medicine)

        return medicine, None

    # =====================================================
    # GET ALL
    # =====================================================

    @staticmethod
    def get_all():
        return MedicineRepository.get_all()

    # =====================================================
    # GET BY ID
    # =====================================================

    @staticmethod
    def get_by_id(medicine_id):
        return MedicineRepository.get_by_id(
            medicine_id
        )

    # =====================================================
    # UPDATE
    # =====================================================

    @staticmethod
    def update(medicine_id, data):

        medicine = MedicineRepository.get_by_id(
            medicine_id
        )

        if not medicine:
            return None

        # Convert expiry date
        if "expiry_date" in data:

            if data["expiry_date"]:

                try:
                    data["expiry_date"] = datetime.strptime(
                        data["expiry_date"],
                        "%Y-%m-%d"
                    ).date()

                except ValueError:
                    return None

            else:
                data["expiry_date"] = None

        # Only allow valid medicine fields
        allowed_fields = [
            "hospital_id",
            "name",
            "generic_name",
            "manufacturer",
            "category",
            "batch_number",
            "expiry_date",
            "price",
            "stock_quantity",
            "minimum_stock",
            "description",
            "is_active"
        ]

        for key, value in data.items():

            if key in allowed_fields:
                setattr(
                    medicine,
                    key,
                    value
                )

        MedicineRepository.update()

        return medicine

    # =====================================================
    # DELETE
    # =====================================================

    @staticmethod
    def delete(medicine_id):

        medicine = MedicineRepository.get_by_id(
            medicine_id
        )

        if not medicine:
            return False

        MedicineRepository.delete(
            medicine
        )

        return True

    # =====================================================
    # SEARCH
    # =====================================================

    @staticmethod
    def search(name):

        return MedicineRepository.search(
            name
        )

    # =====================================================
    # LOW STOCK
    # =====================================================

    @staticmethod
    def low_stock():

        return MedicineRepository.low_stock()