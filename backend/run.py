from app import create_app
from app.extensions import socketio

app = create_app()

with app.app_context():
    try:
        from app.models.hospital import Hospital
        if Hospital.query.count() < 25:
            from seed import seed_database
            seed_database(reset=False)
    except Exception as e:
        print(f"Startup seeder check note: {e}")

if __name__ == "__main__":
    socketio.run(
        app,
        host="127.0.0.1",
        port=5000,
        debug=True,
        allow_unsafe_werkzeug=True
    )