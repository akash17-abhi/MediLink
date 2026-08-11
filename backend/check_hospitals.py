from app import create_app
from app.models.hospital import Hospital

app = create_app()

with app.app_context():
    hospitals = Hospital.query.all()

    print()
    print("===== HOSPITALS =====")

    for hospital in hospitals:
        print(
            f"ID: {hospital.id} | "
            f"Name: {hospital.name} | "
            f"User ID: {hospital.user_id}"
        )

    print("====================")