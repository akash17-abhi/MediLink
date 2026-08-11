from .auth import auth_bp
from .hospital import hospital_bp
from .doctor import doctor_bp
from .doctor_schedule import schedule_bp
from .patient import patient_bp
from .appointment import appointment_bp
from .medical_record import medical_record_bp
from .prescription import prescription_bp
from .medicine import medicine_bp
from .laboratory import laboratory_bp
from .bill import bill_bp
from .payment import payment_bp
from .notification import notification_bp
from .email_test import email_test_bp
from .role import role_bp


def register_routes(app):

    app.register_blueprint(auth_bp)

    app.register_blueprint(hospital_bp)

    app.register_blueprint(doctor_bp)

    app.register_blueprint(schedule_bp)

    app.register_blueprint(patient_bp)

    app.register_blueprint(appointment_bp)

    app.register_blueprint(medical_record_bp)

    app.register_blueprint(prescription_bp)

    app.register_blueprint(medicine_bp)

    app.register_blueprint(laboratory_bp)

    app.register_blueprint(bill_bp)

    app.register_blueprint(payment_bp)

    app.register_blueprint(notification_bp)

    app.register_blueprint(email_test_bp)

    app.register_blueprint(role_bp)