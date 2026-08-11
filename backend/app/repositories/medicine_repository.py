from app.extensions import db
from app.models.medicine import Medicine


class MedicineRepository:

    # =====================================================
    # CREATE
    # =====================================================

    @staticmethod
    def create(medicine):

        db.session.add(medicine)
        db.session.commit()

        return medicine

    # =====================================================
    # GET ALL
    # =====================================================

    @staticmethod
    def get_all():

        return Medicine.query.all()

    # =====================================================
    # GET BY ID
    # =====================================================

    @staticmethod
    def get_by_id(medicine_id):

        return Medicine.query.get(medicine_id)

    # =====================================================
    # GET BY HOSPITAL
    # =====================================================

    @staticmethod
    def get_by_hospital(hospital_id):

        return Medicine.query.filter_by(
            hospital_id=hospital_id
        ).all()

    # =====================================================
    # GET BY NAME
    # =====================================================

    @staticmethod
    def get_by_name(name):

        return Medicine.query.filter(
            Medicine.name.ilike(
                f"%{name}%"
            )
        ).all()

    # =====================================================
    # SEARCH
    # =====================================================

    @staticmethod
    def search(name):

        return Medicine.query.filter(
            Medicine.name.ilike(
                f"%{name}%"
            )
        ).all()

    # =====================================================
    # UPDATE
    # =====================================================

    @staticmethod
    def update():

        db.session.commit()

    # =====================================================
    # DELETE
    # =====================================================

    @staticmethod
    def delete(medicine):

        db.session.delete(medicine)
        db.session.commit()

    # =====================================================
    # LOW STOCK
    # =====================================================

    @staticmethod
    def low_stock():

        return Medicine.query.filter(
            Medicine.stock_quantity <= Medicine.minimum_stock,
            Medicine.is_active == True
        ).all()

    # =====================================================
    # LOW STOCK BY HOSPITAL
    # =====================================================

    @staticmethod
    def get_low_stock(hospital_id):

        return Medicine.query.filter(
            Medicine.hospital_id == hospital_id,
            Medicine.stock_quantity <= Medicine.minimum_stock,
            Medicine.is_active == True
        ).all()