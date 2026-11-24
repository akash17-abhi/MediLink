from datetime import datetime


# =========================================================
# BILL VALIDATOR
# =========================================================

def validate_bill(data):
    """
    Validate incoming bill data.
    """

    # -----------------------------------------------------
    # Request body validation
    # -----------------------------------------------------

    if not data:
        return False, "Request body is required"

    # -----------------------------------------------------
    # Required fields
    # -----------------------------------------------------

    required_fields = [
        "patient_id",
        "doctor_id",
        "hospital_id"
    ]

    for field in required_fields:

        if field not in data:
            return False, f"{field} is required"

        if data[field] is None or data[field] == "":
            return False, f"{field} is required"

    # -----------------------------------------------------
    # ID validation
    # -----------------------------------------------------

    for field in [
        "patient_id",
        "doctor_id",
        "hospital_id"
    ]:

        try:
            value = int(data[field])

            if value <= 0:
                return (
                    False,
                    f"{field} must be a valid positive number"
                )

        except (ValueError, TypeError):

            return (
                False,
                f"{field} must be a valid number"
            )

    # -----------------------------------------------------
    # Charge validation
    # -----------------------------------------------------

    charge_fields = [
        "consultation_charge",
        "laboratory_charge",
        "medicine_charge",
        "other_charge",
        "discount",
        "tax"
    ]

    for field in charge_fields:

        if field not in data or data[field] is None:
            continue

        try:
            value = float(data[field])

        except (ValueError, TypeError):

            return (
                False,
                f"{field} must be a valid number"
            )

        if value < 0:

            return (
                False,
                f"{field} cannot be negative"
            )

    # -----------------------------------------------------
    # Payment status validation
    # -----------------------------------------------------

    valid_payment_statuses = [
        "Pending",
        "Paid",
        "Partially Paid",
        "Failed",
        "Refunded"
    ]

    if data.get("payment_status") is not None:

        payment_status = str(
            data["payment_status"]
        ).strip()

        matched_status = None

        for valid_status in valid_payment_statuses:

            if payment_status.lower() == valid_status.lower():

                matched_status = valid_status
                break

        if matched_status is None:

            return (
                False,
                "Invalid payment_status"
            )

    # -----------------------------------------------------
    # Validation successful
    # -----------------------------------------------------

    return True, ""


# =========================================================
# BILL → DICTIONARY
# =========================================================

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
            bill.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if bill.created_at
            else None
        ),

        "updated_at": (
            bill.updated_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if bill.updated_at
            else None
        )
    }