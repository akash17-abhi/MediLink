from app import create_app
from app.models.user import User


app = create_app()


with app.app_context():

    users = User.query.order_by(
        User.id.asc()
    ).all()

    print()
    print("===== MediLink Users =====")

    if not users:
        print("No users found.")

    else:

        for user in users:

            print(
                f"ID: {user.id} | "
                f"Name: {user.full_name} | "
                f"Email: {user.email}"
            )

    print("==========================")