from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.role import Role


app = create_app()

with app.app_context():

    # Find the user
    user = User.query.get(3)

    if not user:
        print("❌ User ID 3 not found")
        raise SystemExit

    # Find Admin role
    admin_role = Role.query.filter_by(name="Admin").first()

    if not admin_role:
        print("❌ Admin role not found")
        raise SystemExit

    # Check if already assigned
    if admin_role in user.roles:
        print("ℹ️ Admin role is already assigned")
    else:
        user.roles.append(admin_role)
        db.session.commit()

        print("✅ Admin role assigned successfully")

    print()
    print("===== USER =====")
    print("ID:", user.id)
    print("Name:", user.full_name)
    print("Email:", user.email)

    print()
    print("===== ROLES =====")

    for role in user.roles:
        print(
            "Role ID:",
            role.id,
            "| Role:",
            role.name
        )