from app import create_app, db
from sqlalchemy import inspect


app = create_app()


with app.app_context():

    inspector = inspect(db.engine)

    tables = inspector.get_table_names()

    print("\n===== DATABASE TABLES =====")

    for table in tables:
        print(table)

    print("\n===== HOSPITAL TABLE =====")

    if "hospitals" in tables:

        columns = inspector.get_columns("hospitals")

        for column in columns:

            print(
                f"{column['name']} "
                f"| {column['type']} "
                f"| nullable: {column['nullable']}"
            )

    else:

        print("❌ hospitals table does NOT exist")