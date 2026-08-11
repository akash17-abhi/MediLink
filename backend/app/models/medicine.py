from app.extensions import db
from app.models.base_model import BaseModel


class Medicine(BaseModel):

    __tablename__ = "medicines"

    # =========================================================
    # HOSPITAL
    # =========================================================

    hospital_id = db.Column(
        db.Integer,
        db.ForeignKey("hospitals.id"),
        nullable=False
    )

    # =========================================================
    # BASIC INFORMATION
    # =========================================================

    name = db.Column(
        db.String(200),
        nullable=False
    )

    generic_name = db.Column(
        db.String(200)
    )

    manufacturer = db.Column(
        db.String(200)
    )

    category = db.Column(
        db.String(100)
    )

    # =========================================================
    # BATCH INFORMATION
    # =========================================================

    batch_number = db.Column(
        db.String(100)
    )

    expiry_date = db.Column(
        db.Date
    )

    # =========================================================
    # INVENTORY / PRICING
    # =========================================================

    price = db.Column(
        db.Float,
        default=0,
        nullable=False
    )

    stock_quantity = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    minimum_stock = db.Column(
        db.Integer,
        default=10,
        nullable=False
    )

    # =========================================================
    # DESCRIPTION
    # =========================================================

    description = db.Column(
        db.Text
    )

    # =========================================================
    # STATUS
    # =========================================================

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    # =========================================================
    # HOSPITAL RELATIONSHIP
    # =========================================================

    hospital = db.relationship(
        "Hospital",
        backref="medicines"
    )

    # =========================================================
    # REPRESENTATION
    # =========================================================

    def __repr__(self):
        return f"<Medicine {self.name}>"