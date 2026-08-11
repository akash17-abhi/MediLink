from app.extensions import db
from app.models.base_model import BaseModel


class DoctorSchedule(BaseModel):

    __tablename__ = "doctor_schedules"

    # =========================================================
    # DOCTOR
    # =========================================================

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey("doctors.id"),
        nullable=False
    )

    # =========================================================
    # DAY
    # =========================================================

    day_of_week = db.Column(
        db.String(20),
        nullable=False
    )

    # =========================================================
    # WORKING TIME
    # =========================================================

    start_time = db.Column(
        db.Time,
        nullable=False
    )

    end_time = db.Column(
        db.Time,
        nullable=False
    )

    # =========================================================
    # APPOINTMENT SLOT
    # =========================================================

    slot_duration = db.Column(
        db.Integer,
        default=30,
        nullable=False
    )

    # =========================================================
    # BREAK TIME
    # =========================================================

    break_start = db.Column(
        db.Time,
        nullable=True
    )

    break_end = db.Column(
        db.Time,
        nullable=True
    )

    # =========================================================
    # STATUS
    # =========================================================

    is_available = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    # =========================================================
    # DOCTOR RELATIONSHIP
    # =========================================================

    doctor = db.relationship(
        "Doctor",
        back_populates="schedules"
    )

    # =========================================================
    # REPRESENTATION
    # =========================================================

    def __repr__(self):
        return (
            f"<DoctorSchedule "
            f"Doctor={self.doctor_id} "
            f"Day={self.day_of_week}>"
        )