from app import create_app
from app.models.user import User

app = create_app()

with app.app_context():

    user = User.query.get(3)

    if not user:
        print("User ID 3 not found")
    else:
        print("===== USER =====")
        print("ID:", user.id)
        print("Name:", user.full_name)
        print("Email:", user.email)
        print("Verified:", user.is_email_verified)

        print("\n===== ROLES =====")

        if user.roles:
            for role in user.roles:
                print(
                    "Role ID:",
                    role.id,
                    "| Role:",
                    role.name
                )
        else:
            print("NO ROLES ASSIGNED")