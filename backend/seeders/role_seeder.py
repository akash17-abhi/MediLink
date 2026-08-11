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
            "description": "Patient / Normal User"
        },
        {
            "name": "Hospital",
            "description": "Hospital / Nursing Home"
        },
        {
            "name": "Laboratory",
            "description": "Laboratory / Diagnostic Center"
        },
        {
            "name": "Ambulance Owner",
            "description": "Ambulance Service Provider"
        }
    ]

    created_count = 0

    for role_data in roles:

        role = Role.query.filter_by(
            name=role_data["name"]
        ).first()

        if not role:

            db.session.add(
                Role(**role_data)
            )

            created_count += 1

            print(
                f"✅ Created role: {role_data['name']}"
            )

        else:

            print(
                f"ℹ️ Role already exists: {role_data['name']}"
            )

    db.session.commit()

    print()
    print(
        f"✅ Role seeding completed. "
        f"{created_count} new role(s) created."
    )