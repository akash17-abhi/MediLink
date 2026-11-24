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
# =========================================================
# CHATBOT
# =========================================================

from .chatbot import chatbot_bp

# =========================================================
# AMBULANCE
# =========================================================

from .ambulance_routes import ambulance_bp

# =========================================================
# EMERGENCY MANAGEMENT
# =========================================================

from .emergency_routes import emergency_bp
from .bed_routes import bed_bp
from .recommendation_routes import recommend_bp
from .hospital_admin_routes import hospital_admin_bp
from .admin_portal_routes import admin_portal_bp
from .patient_portal_routes import patient_portal_bp

# =========================================================
# REGISTER ALL ROUTES
# =========================================================

def register_routes(app):

    # -----------------------------------------------------
    # Authentication
    # -----------------------------------------------------

    app.register_blueprint(
        auth_bp
    )

    # -----------------------------------------------------
    # Hospitals
    # -----------------------------------------------------

    app.register_blueprint(
        hospital_bp
    )

    # -----------------------------------------------------
    # Doctors
    # -----------------------------------------------------

    app.register_blueprint(
        doctor_bp
    )

    # -----------------------------------------------------
    # Doctor Schedules
    # -----------------------------------------------------

    app.register_blueprint(
        schedule_bp
    )

    # -----------------------------------------------------
    # Patients
    # -----------------------------------------------------

    app.register_blueprint(
        patient_bp
    )

    # -----------------------------------------------------
    # Appointments
    # -----------------------------------------------------

    app.register_blueprint(
        appointment_bp
    )

    # -----------------------------------------------------
    # Medical Records
    # -----------------------------------------------------

    app.register_blueprint(
        medical_record_bp
    )

    # -----------------------------------------------------
    # Prescriptions
    # -----------------------------------------------------

    app.register_blueprint(
        prescription_bp
    )

    # -----------------------------------------------------
    # Medicines
    # -----------------------------------------------------

    app.register_blueprint(
        medicine_bp
    )

    # -----------------------------------------------------
    # Laboratory
    # -----------------------------------------------------

    app.register_blueprint(
        laboratory_bp
    )

    # -----------------------------------------------------
    # Bills
    # -----------------------------------------------------

    app.register_blueprint(
        bill_bp
    )

    # -----------------------------------------------------
    # Payments
    # -----------------------------------------------------

    app.register_blueprint(
        payment_bp
    )

    # -----------------------------------------------------
    # Notifications
    # -----------------------------------------------------

    app.register_blueprint(
        notification_bp
    )

    # -----------------------------------------------------
    # Email Testing
    # -----------------------------------------------------

    app.register_blueprint(
        email_test_bp
    )

    # -----------------------------------------------------
    # Roles
    # -----------------------------------------------------

    app.register_blueprint(
        role_bp
    )

    # -----------------------------------------------------
    # MediLink AI Assistant
    # -----------------------------------------------------

    app.register_blueprint(
        chatbot_bp
    )

    # -----------------------------------------------------
    # Ambulances
    # -----------------------------------------------------

    app.register_blueprint(
        ambulance_bp
    )

    # -----------------------------------------------------
    # Emergency Management
    # -----------------------------------------------------

    app.register_blueprint(
        emergency_bp
    )

    # -----------------------------------------------------
    # Beds
    # -----------------------------------------------------

    app.register_blueprint(
        bed_bp
    )

    # -----------------------------------------------------
    # Recommendation & Emergency Search
    # -----------------------------------------------------

    app.register_blueprint(
        recommend_bp
    )

    # -----------------------------------------------------
    # Hospital / Clinic Management Portal
    # -----------------------------------------------------

    app.register_blueprint(
        hospital_admin_bp
    )

    # -----------------------------------------------------
    # Super Admin Overview Portal
    # -----------------------------------------------------

    app.register_blueprint(
        admin_portal_bp
    )

    # -----------------------------------------------------
    # Patient Appointments & Emergency Portal
    # -----------------------------------------------------

    app.register_blueprint(
        patient_portal_bp
    )