from marshmallow import Schema, fields, validate


# =========================================================
# BED CREATE SCHEMA
# =========================================================

class BedCreateSchema(Schema):

    hospital_id = fields.Integer(
        required=True
    )

    bed_number = fields.String(
        required=True,
        validate=validate.Length(min=1, max=50)
    )

    ward = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    bed_type = fields.String(
        required=True,
        validate=validate.OneOf([
            "General",
            "ICU",
            "Emergency",
            "Private",
            "Semi-Private",
            "Pediatric",
            "Maternity",
            "Isolation"
        ])
    )

    floor = fields.String(
        required=False,
        allow_none=True
    )

    room_number = fields.String(
        required=False,
        allow_none=True
    )

    status = fields.String(
        required=False,
        validate=validate.OneOf([
            "Available",
            "Occupied",
            "Reserved",
            "Maintenance",
            "Blocked"
        ]),
        load_default="Available"
    )

    patient_id = fields.Integer(
        required=False,
        allow_none=True
    )

    notes = fields.String(
        required=False,
        allow_none=True
    )


# =========================================================
# BED UPDATE SCHEMA
# =========================================================

class BedUpdateSchema(Schema):

    bed_number = fields.String(
        required=False,
        validate=validate.Length(min=1, max=50)
    )

    ward = fields.String(
        required=False,
        validate=validate.Length(min=1, max=100)
    )

    bed_type = fields.String(
        required=False,
        validate=validate.OneOf([
            "General",
            "ICU",
            "Emergency",
            "Private",
            "Semi-Private",
            "Pediatric",
            "Maternity",
            "Isolation"
        ])
    )

    floor = fields.String(
        required=False,
        allow_none=True
    )

    room_number = fields.String(
        required=False,
        allow_none=True
    )

    status = fields.String(
        required=False,
        validate=validate.OneOf([
            "Available",
            "Occupied",
            "Reserved",
            "Maintenance",
            "Blocked"
        ])
    )

    patient_id = fields.Integer(
        required=False,
        allow_none=True
    )

    notes = fields.String(
        required=False,
        allow_none=True
    )


# =========================================================
# BED STATUS UPDATE SCHEMA
# =========================================================

class BedStatusSchema(Schema):

    status = fields.String(
        required=True,
        validate=validate.OneOf([
            "Available",
            "Occupied",
            "Reserved",
            "Maintenance",
            "Blocked"
        ])
    )


# =========================================================
# BED PATIENT ASSIGNMENT SCHEMA
# =========================================================

class BedAssignPatientSchema(Schema):

    patient_id = fields.Integer(
        required=True
    )


# =========================================================
# BED RESPONSE SCHEMA
# =========================================================

class BedResponseSchema(Schema):

    id = fields.Integer()

    hospital_id = fields.Integer()

    bed_number = fields.String()

    ward = fields.String()

    bed_type = fields.String()

    floor = fields.String(
        allow_none=True
    )

    room_number = fields.String(
        allow_none=True
    )

    status = fields.String()

    patient_id = fields.Integer(
        allow_none=True
    )

    notes = fields.String(
        allow_none=True
    )

    created_at = fields.String(
        allow_none=True
    )

    updated_at = fields.String(
        allow_none=True
    )