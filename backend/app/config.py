import os


BASE_DIR = os.path.abspath(
    os.path.dirname(os.path.dirname(__file__))
)


class Config:

    # =========================================================
    # FLASK
    # =========================================================

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "medilink-development-secret-key"
    )

    # =========================================================
    # DATABASE CONFIGURATION (Default to SQLite for instant local run)
    # =========================================================

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "medilink.db").replace("\\", "/")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =========================================================
    # JWT
    # =========================================================

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "medilink-jwt-secret-key"
    )

    # =========================================================
    # EMAIL CONFIGURATION
    # =========================================================

    MAIL_SERVER = os.getenv(
        "MAIL_SERVER",
        "smtp.gmail.com"
    )

    MAIL_PORT = int(
        os.getenv(
            "MAIL_PORT",
            587
        )
    )

    MAIL_USE_TLS = (
        os.getenv(
            "MAIL_USE_TLS",
            "True"
        ).lower() == "true"
    )

    MAIL_USERNAME = os.getenv(
        "MAIL_USERNAME",
        ""
    )

    MAIL_PASSWORD = os.getenv(
        "MAIL_PASSWORD",
        ""
    )

    MAIL_DEFAULT_SENDER = os.getenv(
        "MAIL_DEFAULT_SENDER",
        ""
    )