from app import create_app
from app.extensions import db
from app.models.hospital import Hospital
from app.models.user import User


app = create_app()


with app.app_context():

    # =====================================================
    # IDs
    # =====================================================

    USER_ID = 3
    HOSPITAL_ID = 2

    # =====================================================
    # Find user
    # =====================================================

    user = db.session.get(User, USER_ID)

    if not user:
        print("❌ User not found.")
        exit()

    print(
        f"User found: {user.id} | "
        f"{user.full_name} | "
        f"{user.email}"
    )

    # =====================================================
    # Find hospital
    # =====================================================

    hospital = db.session.get(
        Hospital,
        HOSPITAL_ID
    )

    if not hospital:
        print("❌ Hospital not found.")
        exit()

    print(
        f"Hospital found: {hospital.id} | "
        f"{hospital.name}"
    )

    # =====================================================
    # Check existing hospital owner
    # =====================================================

    if hospital.user_id is not None:

        print(
            f"⚠️ Hospital is already assigned "
            f"to User ID {hospital.user_id}"
        )

        exit()

    # =====================================================
    # Check whether user already owns a hospital
    # =====================================================

    existing_hospital = Hospital.query.filter(
        Hospital.user_id == USER_ID
    ).first()

    if existing_hospital:

        print(
            f"⚠️ User already owns "
            f"Hospital ID {existing_hospital.id}: "
            f"{existing_hospital.name}"
        )

        exit()

    # =====================================================
    # Assign hospital
    # =====================================================

    hospital.user_id = user.id

    db.session.commit()

    print("\n✅ Hospital assigned successfully!")

    print(
        f"User ID: {user.id}"
    )

    print(
        f"User Email: {user.email}"
    )

    print(
        f"Hospital ID: {hospital.id}"
    )

    print(
        f"Hospital Name: {hospital.name}"
    )