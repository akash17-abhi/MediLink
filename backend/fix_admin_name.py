from app import create_app
from app.extensions import db
from app.models.user import User


app = create_app()

with app.app_context():

    user = User.query.filter_by(
        email="medilink.officialadmin.ap@gmail.com"
    ).first()

    if not user:
        print("❌ Admin user not found")
        raise SystemExit

    print("===== BEFORE =====")
    print("ID:", user.id)
    print("Name:", user.full_name)
    print("Email:", user.email)

    user.full_name = "MediLink Administrator"

    db.session.commit()

    print()
    print("✅ Admin name updated successfully")

    print()
    print("===== AFTER =====")
    print("ID:", user.id)
    print("Name:", user.full_name)
    print("Email:", user.email)