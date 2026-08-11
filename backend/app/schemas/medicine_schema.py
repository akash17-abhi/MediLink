def validate_medicine(data):

    required_fields = [
        "hospital_id",
        "name"
    ]

    # =====================================================
    # REQUIRED FIELDS
    # =====================================================

    for field in required_fields:

        if field not in data or data[field] in (None, ""):
            return False, f"{field} is required"

    # =====================================================
    # PRICE VALIDATION
    # =====================================================

    if "price" in data and data["price"] is not None:

        try:
            price = float(data["price"])

            if price < 0:
                return False, "price cannot be negative"

        except (TypeError, ValueError):
            return False, "price must be a valid number"

    # =====================================================
    # STOCK VALIDATION
    # =====================================================

    if "stock_quantity" in data and data["stock_quantity"] is not None:

        try:
            stock_quantity = int(data["stock_quantity"])

            if stock_quantity < 0:
                return False, "stock_quantity cannot be negative"

        except (TypeError, ValueError):
            return False, "stock_quantity must be a valid integer"

    # =====================================================
    # MINIMUM STOCK VALIDATION
    # =====================================================

    if "minimum_stock" in data and data["minimum_stock"] is not None:

        try:
            minimum_stock = int(data["minimum_stock"])

            if minimum_stock < 0:
                return False, "minimum_stock cannot be negative"

        except (TypeError, ValueError):
            return False, "minimum_stock must be a valid integer"

    # =====================================================
    # ACTIVE STATUS VALIDATION
    # =====================================================

    if "is_active" in data:

        if not isinstance(data["is_active"], bool):
            return False, "is_active must be true or false"

    return True, ""


def medicine_to_dict(medicine):

    return {
        "id": medicine.id,

        "hospital_id": medicine.hospital_id,

        "name": medicine.name,

        "generic_name": medicine.generic_name,

        "manufacturer": medicine.manufacturer,

        "category": medicine.category,

        "batch_number": medicine.batch_number,

        "expiry_date": (
            medicine.expiry_date.strftime("%Y-%m-%d")
            if medicine.expiry_date
            else None
        ),

        "price": medicine.price,

        "stock_quantity": medicine.stock_quantity,

        "minimum_stock": medicine.minimum_stock,

        "description": medicine.description,

        "is_active": medicine.is_active,

        "created_at": (
            medicine.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if medicine.created_at
            else None
        ),

        "updated_at": (
            medicine.updated_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if medicine.updated_at
            else None
        )
    }