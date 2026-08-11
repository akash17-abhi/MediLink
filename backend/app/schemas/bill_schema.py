def validate_bill(data):

    required_fields = [
        "patient_id",
        "doctor_id",
        "hospital_id"
    ]

    for field in required_fields:
        if field not in data or data[field] in (None, ""):
            return False, f"{field} is required"

    return True, ""


def bill_to_dict(bill):

    return {
        "id": bill.id,
        "patient_id": bill.patient_id,
        "doctor_id": bill.doctor_id,
        "hospital_id": bill.hospital_id,
        "consultation_charge": bill.consultation_charge,
        "laboratory_charge": bill.laboratory_charge,
        "medicine_charge": bill.medicine_charge,
        "other_charge": bill.other_charge,
        "discount": bill.discount,
        "tax": bill.tax,
        "total_amount": bill.total_amount,
        "payment_status": bill.payment_status,
        "created_at": (
            bill.created_at.strftime("%Y-%m-%d %H:%M:%S")
            if bill.created_at else None
        ),
        "updated_at": (
            bill.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            if bill.updated_at else None
        )
    }