from app.extensions import db
from app.models.role import Role


def seed_roles():

    roles = [
        {
            "name": "Admin",
            "description": "System Administrator"
        },
        {
            "name": "Doctor",
            "description": "Medical Practitioner"
        },
        {
            "name": "Patient",
            "description": "Normal User"
        },
        {
            "name": "Hospital",
            "description": "Hospital / Nursing Home"
        },
        {
            "name": "Ambulance Owner",
            "description": "Ambulance Service Provider"
        }
    ]

    for role_data in roles:

        role = Role.query.filter_by(name=role_data["name"]).first()

        if not role:

            db.session.add(Role(**role_data))

    db.session.commit()

    print("✅ Default roles created successfully.")