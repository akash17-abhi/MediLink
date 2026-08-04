from app import create_app
from app.extensions import db
from seeders.role_seeder import seed_roles

app = create_app()

with app.app_context():

    db.create_all()

    seed_roles()

    print("✅ Database seeded successfully.")