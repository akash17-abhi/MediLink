# backend/app/services/email_service.py

from flask import current_app
from flask_mail import Mail, Message


mail = Mail()


class EmailService:
    """Service responsible for sending MediLink emails."""

    @staticmethod
    def init_app(app):
        """Initialize Flask-Mail."""
        mail.init_app(app)

    @staticmethod
    def send_email(
        recipient,
        subject,
        body,
        html=None
    ):
        """
        Send an email.

        Returns:
            (True, None) if successful
            (False, error_message) if failed
        """

        try:
            if not recipient:
                return False, "Recipient email is required"

            message = Message(
                subject=subject,
                recipients=[recipient],
                sender=current_app.config["MAIL_DEFAULT_SENDER"]
            )

            message.body = body

            if html:
                message.html = html

            mail.send(message)

            return True, None

        except Exception as e:
            current_app.logger.error(
                f"Email sending failed: {str(e)}"
            )

            return False, str(e)

    # ---------------------------------------------------------
    # TEST EMAIL
    # ---------------------------------------------------------

    @staticmethod
    def send_test_email(recipient):
        """Send a simple test email."""

        subject = "MediLink - Test Email"

        body = """
Hello,

This is a test email from MediLink.

Your MediLink email service has been configured successfully.

Regards,
MediLink Team
"""

        html = """
        <html>
            <body>
                <h2>MediLink - Test Email</h2>

                <p>Hello,</p>

                <p>
                    This is a test email from
                    <strong>MediLink</strong>.
                </p>

                <p>
                    Your MediLink email service has been
                    configured successfully.
                </p>

                <br>

                <p>
                    Regards,<br>
                    <strong>MediLink Team</strong>
                </p>
            </body>
        </html>
        """

        return EmailService.send_email(
            recipient=recipient,
            subject=subject,
            body=body,
            html=html
        )

    # ---------------------------------------------------------
    # APPOINTMENT CONFIRMED
    # ---------------------------------------------------------

    @staticmethod
    def send_appointment_confirmation(
        patient_email,
        patient_name,
        doctor_name,
        appointment_date,
        appointment_time,
        hospital_name=None
    ):
        """Send appointment confirmation email."""

        subject = "MediLink - Appointment Confirmed"

        hospital_text = hospital_name or "MediLink Hospital"

        body = f"""
Dear {patient_name},

Your appointment has been successfully confirmed.

Appointment Details
-------------------

Doctor: {doctor_name}
Date: {appointment_date}
Time: {appointment_time}
Hospital: {hospital_text}

Please arrive a few minutes before your scheduled appointment time.

If you need to cancel or reschedule your appointment, please use the MediLink platform.

Regards,
MediLink Team
"""

        html = f"""
        <html>
            <body style="
                font-family: Arial, sans-serif;
                line-height: 1.6;
            ">

                <h2>MediLink - Appointment Confirmed</h2>

                <p>
                    Dear <strong>{patient_name}</strong>,
                </p>

                <p>
                    Your appointment has been
                    <strong>successfully confirmed</strong>.
                </p>

                <h3>Appointment Details</h3>

                <table
                    border="1"
                    cellpadding="8"
                    cellspacing="0"
                    style="border-collapse: collapse;"
                >
                    <tr>
                        <td><strong>Doctor</strong></td>
                        <td>{doctor_name}</td>
                    </tr>

                    <tr>
                        <td><strong>Date</strong></td>
                        <td>{appointment_date}</td>
                    </tr>

                    <tr>
                        <td><strong>Time</strong></td>
                        <td>{appointment_time}</td>
                    </tr>

                    <tr>
                        <td><strong>Hospital</strong></td>
                        <td>{hospital_text}</td>
                    </tr>
                </table>

                <p>
                    Please arrive a few minutes before
                    your scheduled appointment time.
                </p>

                <p>
                    If you need to cancel or reschedule
                    your appointment, please use the
                    MediLink platform.
                </p>

                <br>

                <p>
                    Regards,<br>
                    <strong>MediLink Team</strong>
                </p>

            </body>
        </html>
        """

        return EmailService.send_email(
            recipient=patient_email,
            subject=subject,
            body=body,
            html=html
        )

    # ---------------------------------------------------------
    # APPOINTMENT CANCELLED
    # ---------------------------------------------------------

    @staticmethod
    def send_appointment_cancellation(
        patient_email,
        patient_name,
        doctor_name,
        appointment_date,
        appointment_time,
        reason=None
    ):
        """Send appointment cancellation email."""

        subject = "MediLink - Appointment Cancelled"

        cancellation_reason = reason or "No reason was provided."

        body = f"""
Dear {patient_name},

Your appointment has been cancelled.

Appointment Details
-------------------

Doctor: {doctor_name}
Date: {appointment_date}
Time: {appointment_time}

Reason:
{cancellation_reason}

Please use MediLink to book another appointment if required.

Regards,
MediLink Team
"""

        html = f"""
        <html>
            <body style="
                font-family: Arial, sans-serif;
                line-height: 1.6;
            ">

                <h2>MediLink - Appointment Cancelled</h2>

                <p>
                    Dear <strong>{patient_name}</strong>,
                </p>

                <p>
                    Your appointment has been
                    <strong>cancelled</strong>.
                </p>

                <h3>Appointment Details</h3>

                <p>
                    <strong>Doctor:</strong> {doctor_name}<br>
                    <strong>Date:</strong> {appointment_date}<br>
                    <strong>Time:</strong> {appointment_time}
                </p>

                <h3>Reason</h3>

                <p>{cancellation_reason}</p>

                <p>
                    Please use MediLink to book another
                    appointment if required.
                </p>

                <br>

                <p>
                    Regards,<br>
                    <strong>MediLink Team</strong>
                </p>

            </body>
        </html>
        """

        return EmailService.send_email(
            recipient=patient_email,
            subject=subject,
            body=body,
            html=html
        )