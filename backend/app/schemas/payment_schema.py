from datetime import datetime


# =========================================================
# PAYMENT VALIDATOR
# =========================================================

def validate_payment(data):

    # -----------------------------------------------------
    # Check request body
    # -----------------------------------------------------

    if not data:
        return False, "Request body is required"

    # -----------------------------------------------------
    # Required fields
    # -----------------------------------------------------

    required_fields = [
        "bill_id",
        "amount",
        "payment_method"
    ]

    for field in required_fields:

        if field not in data:
            return False, f"{field} is required"

        if data[field] is None:
            return False, f"{field} is required"

        if isinstance(data[field], str) and not data[field].strip():
            return False, f"{field} cannot be empty"

    # =====================================================
    # BILL ID VALIDATION
    # =====================================================

    try:

        bill_id = int(data["bill_id"])

        if bill_id <= 0:
            return (
                False,
                "bill_id must be a valid positive number"
            )

    except (ValueError, TypeError):

        return (
            False,
            "bill_id must be a valid number"
        )

    # =====================================================
    # AMOUNT VALIDATION
    # =====================================================

    try:

        amount = float(data["amount"])

        if amount <= 0:

            return (
                False,
                "amount must be greater than 0"
            )

    except (ValueError, TypeError):

        return (
            False,
            "amount must be a valid number"
        )

    # =====================================================
    # PAYMENT METHOD VALIDATION
    # =====================================================

    payment_method = str(
        data["payment_method"]
    ).strip()

    valid_payment_methods = [
        "Cash",
        "Card",
        "UPI",
        "Net Banking",
        "Insurance"
    ]

    matched_method = None

    for method in valid_payment_methods:

        if payment_method.lower() == method.lower():

            matched_method = method
            break

    if matched_method is None:

        return (
            False,
            "payment_method must be Cash, Card, UPI, Net Banking, or Insurance"
        )

    # =====================================================
    # TRANSACTION ID VALIDATION
    # =====================================================

    if data.get("transaction_id") is not None:

        transaction_id = str(
            data["transaction_id"]
        ).strip()

        if not transaction_id:

            return (
                False,
                "transaction_id cannot be empty"
            )

        if len(transaction_id) > 150:

            return (
                False,
                "transaction_id cannot exceed 150 characters"
            )

    # =====================================================
    # PAYMENT STATUS VALIDATION
    # =====================================================

    valid_statuses = [
        "Pending",
        "Completed",
        "Failed",
        "Refunded"
    ]

    if data.get("payment_status") is not None:

        payment_status = str(
            data["payment_status"]
        ).strip()

        matched_status = None

        for status in valid_statuses:

            if payment_status.lower() == status.lower():

                matched_status = status
                break

        if matched_status is None:

            return (
                False,
                "Invalid payment_status"
            )

    # =====================================================
    # PAYMENT DATE VALIDATION
    # =====================================================

    if data.get("payment_date") is not None:

        payment_date = data["payment_date"]

        if isinstance(payment_date, datetime):

            pass

        elif isinstance(payment_date, str):

            try:

                datetime.strptime(
                    payment_date.strip(),
                    "%Y-%m-%d %H:%M:%S"
                )

            except ValueError:

                return (
                    False,
                    "payment_date must be in YYYY-MM-DD HH:MM:SS format"
                )

        else:

            return (
                False,
                "payment_date must be in YYYY-MM-DD HH:MM:SS format"
            )

    # =====================================================
    # REMARKS VALIDATION
    # =====================================================

    if data.get("remarks") is not None:

        remarks = str(
            data["remarks"]
        ).strip()

        if len(remarks) > 1000:

            return (
                False,
                "remarks cannot exceed 1000 characters"
            )

    # =====================================================
    # VALIDATION SUCCESSFUL
    # =====================================================

    return True, ""


# =========================================================
# PAYMENT → DICTIONARY
# =========================================================

def payment_to_dict(payment):

    return {

        # -------------------------------------------------
        # Basic information
        # -------------------------------------------------

        "id": payment.id,

        "bill_id": payment.bill_id,

        "amount": payment.amount,

        "payment_method": payment.payment_method,

        "transaction_id": payment.transaction_id,

        "payment_status": payment.payment_status,

        # -------------------------------------------------
        # Payment date
        # -------------------------------------------------

        "payment_date": (
            payment.payment_date.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if payment.payment_date
            else None
        ),

        # -------------------------------------------------
        # Remarks
        # -------------------------------------------------

        "remarks": payment.remarks,

        # -------------------------------------------------
        # Timestamps
        # -------------------------------------------------

        "created_at": (
            payment.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if payment.created_at
            else None
        ),

        "updated_at": (
            payment.updated_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if payment.updated_at
            else None
        )
    }