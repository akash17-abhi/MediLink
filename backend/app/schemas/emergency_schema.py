from marshmallow import Schema, fields, validate


class EmergencyCreateSchema(Schema):
    """Validation schema for creating an emergency request."""

    patient_id = fields.Integer(
        required=True
    )

    hospital_id = fields.Integer(
        required=False,
        allow_none=True
    )

    ambulance_id = fields.Integer(
        required=False,
        allow_none=True
    )

    emergency_type = fields.String(
        required=True,
        validate=validate.Length(
            min=2,
            max=100
        )
    )

    description = fields.String(
        required=False,
        allow_none=True
    )

    priority = fields.String(
        required=False,
        load_default="Medium",
        validate=validate.OneOf([
            "Low",
            "Medium",
            "High",
            "Critical"
        ])
    )

    pickup_location = fields.String(
        required=True,
        validate=validate.Length(
            min=2,
            max=500
        )
    )

    destination = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(
            min=2,
            max=500
        )
    )


class EmergencyUpdateSchema(Schema):
    """Validation schema for updating an emergency."""

    hospital_id = fields.Integer(
        required=False,
        allow_none=True
    )

    ambulance_id = fields.Integer(
        required=False,
        allow_none=True
    )

    emergency_type = fields.String(
        required=False,
        validate=validate.Length(
            min=2,
            max=100
        )
    )

    description = fields.String(
        required=False,
        allow_none=True
    )

    priority = fields.String(
        required=False,
        validate=validate.OneOf([
            "Low",
            "Medium",
            "High",
            "Critical"
        ])
    )

    pickup_location = fields.String(
        required=False,
        validate=validate.Length(
            min=2,
            max=500
        )
    )

    destination = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(
            min=2,
            max=500
        )
    )


class AssignAmbulanceSchema(Schema):
    """Validation schema for assigning an ambulance."""

    ambulance_id = fields.Integer(
        required=True
    )


class AssignHospitalSchema(Schema):
    """Validation schema for assigning a hospital."""

    hospital_id = fields.Integer(
        required=True
    )