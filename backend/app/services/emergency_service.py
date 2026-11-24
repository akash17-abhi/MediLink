from app.extensions import db
from app.models.emergency import Emergency
from app.models.patient import Patient
from app.models.hospital import Hospital
from app.models.ambulance import Ambulance
from app.repositories.emergency_repository import EmergencyRepository


class EmergencyService:
    """Business logic for MediLink emergency management."""

    ACTIVE_STATUSES = [
        "Requested",
        "Assigned",
        "Dispatched",
        "On The Way",
        "Arrived",
        "Patient Picked Up",
        "Hospital Arrived",
    ]

    # =========================================================
    # CREATE EMERGENCY
    # =========================================================

    @staticmethod
    def create_emergency(data):

        patient_id = data.get("patient_id")

        if not patient_id:
            return None, "Patient ID is required"

        patient = Patient.query.get(patient_id)

        if not patient:
            return None, "Patient not found"

        if not patient.active:
            return None, "Patient account is inactive"

        emergency_type = data.get("emergency_type")

        if not emergency_type:
            return None, "Emergency type is required"

        pickup_location = data.get("pickup_location")

        if not pickup_location:
            return None, "Pickup location is required"

        priority = data.get("priority", "Medium")

        allowed_priorities = [
            "Low",
            "Medium",
            "High",
            "Critical"
        ]

        if priority not in allowed_priorities:
            return None, (
                "Invalid priority. Allowed values: "
                "Low, Medium, High, Critical"
            )

        emergency = Emergency(
            patient_id=patient_id,
            hospital_id=data.get("hospital_id"),
            ambulance_id=data.get("ambulance_id"),
            emergency_type=emergency_type,
            description=data.get("description"),
            priority=priority,
            pickup_location=pickup_location,
            destination=data.get("destination"),
            status="Requested",
        )

        emergency = EmergencyRepository.create(emergency)

        return emergency, None

    # =========================================================
    # GET EMERGENCY
    # =========================================================

    @staticmethod
    def get_emergency(emergency_id):

        emergency = EmergencyRepository.get_by_id(
            emergency_id
        )

        if not emergency:
            return None, "Emergency request not found"

        return emergency, None

    # =========================================================
    # GET ALL
    # =========================================================

    @staticmethod
    def get_all_emergencies():

        return EmergencyRepository.get_all()

    # =========================================================
    # GET PATIENT EMERGENCIES
    # =========================================================

    @staticmethod
    def get_patient_emergencies(patient_id):

        patient = Patient.query.get(patient_id)

        if not patient:
            return None, "Patient not found"

        return EmergencyRepository.get_by_patient(
            patient_id
        ), None

    # =========================================================
    # GET HOSPITAL EMERGENCIES
    # =========================================================

    @staticmethod
    def get_hospital_emergencies(hospital_id):

        hospital = Hospital.query.get(hospital_id)

        if not hospital:
            return None, "Hospital not found"

        return EmergencyRepository.get_by_hospital(
            hospital_id
        ), None

    # =========================================================
    # GET ACTIVE EMERGENCIES
    # =========================================================

    @staticmethod
    def get_active_emergencies():

        return EmergencyRepository.get_active()

    # =========================================================
    # GET PENDING EMERGENCIES
    # =========================================================

    @staticmethod
    def get_pending_emergencies():

        return EmergencyRepository.get_pending()

    # =========================================================
    # ASSIGN AMBULANCE
    # =========================================================

    @staticmethod
    def assign_ambulance(emergency_id, ambulance_id):

        emergency = EmergencyRepository.get_by_id(
            emergency_id
        )

        if not emergency:
            return None, "Emergency request not found"

        if emergency.status not in [
            "Requested",
            "Assigned"
        ]:
            return None, (
                f"Ambulance cannot be assigned when "
                f"emergency status is '{emergency.status}'"
            )

        ambulance = Ambulance.query.get(ambulance_id)

        if not ambulance:
            return None, "Ambulance not found"

        if ambulance.availability_status != "Available":
            return None, "Ambulance is not available"

        if ambulance.emergency_status != "Normal":
            return None, "Ambulance is currently handling an emergency"

        # If a hospital is already selected, ensure ambulance
        # belongs to that hospital.
        if (
            emergency.hospital_id
            and ambulance.hospital_id != emergency.hospital_id
        ):
            return None, (
                "Ambulance does not belong to the selected hospital"
            )

        emergency.ambulance_id = ambulance.id

        ambulance.availability_status = "Busy"
        ambulance.emergency_status = "Emergency"

        emergency.status = "Assigned"

        EmergencyRepository.update(emergency)

        return emergency, None

    # =========================================================
    # ASSIGN HOSPITAL
    # =========================================================

    @staticmethod
    def assign_hospital(emergency_id, hospital_id):

        emergency = EmergencyRepository.get_by_id(
            emergency_id
        )

        if not emergency:
            return None, "Emergency request not found"

        hospital = Hospital.query.get(hospital_id)

        if not hospital:
            return None, "Hospital not found"

        if not hospital.is_active:
            return None, "Hospital is currently inactive"

        emergency.hospital_id = hospital.id

        if not emergency.destination:
            emergency.destination = hospital.address

        EmergencyRepository.update(emergency)

        return emergency, None

    # =========================================================
    # DISPATCH AMBULANCE
    # =========================================================

    @staticmethod
    def dispatch(emergency_id):

        emergency = EmergencyRepository.get_by_id(
            emergency_id
        )

        if not emergency:
            return None, "Emergency request not found"

        if emergency.status != "Assigned":
            return None, (
                "Only an assigned emergency can be dispatched"
            )

        if not emergency.ambulance_id:
            return None, "No ambulance assigned"

        ambulance = Ambulance.query.get(
            emergency.ambulance_id
        )

        if not ambulance:
            return None, "Assigned ambulance not found"

        emergency.status = "Dispatched"

        ambulance.availability_status = "Busy"
        ambulance.emergency_status = "Emergency"

        EmergencyRepository.update(emergency)

        return emergency, None

    # =========================================================
    # ON THE WAY
    # =========================================================

    @staticmethod
    def mark_on_the_way(emergency_id):

        emergency = EmergencyRepository.get_by_id(
            emergency_id
        )

        if not emergency:
            return None, "Emergency request not found"

        if emergency.status != "Dispatched":
            return None, (
                "Emergency must be dispatched first"
            )

        emergency.status = "On The Way"

        EmergencyRepository.update(emergency)

        return emergency, None

    # =========================================================
    # ARRIVED
    # =========================================================

    @staticmethod
    def mark_arrived(emergency_id):

        emergency = EmergencyRepository.get_by_id(
            emergency_id
        )

        if not emergency:
            return None, "Emergency request not found"

        if emergency.status != "On The Way":
            return None, (
                "Ambulance must be on the way first"
            )

        emergency.status = "Arrived"

        EmergencyRepository.update(emergency)

        return emergency, None

    # =========================================================
    # PATIENT PICKED UP
    # =========================================================

    @staticmethod
    def mark_patient_picked_up(emergency_id):

        emergency = EmergencyRepository.get_by_id(
            emergency_id
        )

        if not emergency:
            return None, "Emergency request not found"

        if emergency.status != "Arrived":
            return None, (
                "Ambulance must arrive before "
                "patient can be picked up"
            )

        emergency.status = "Patient Picked Up"

        EmergencyRepository.update(emergency)

        return emergency, None

    # =========================================================
    # HOSPITAL ARRIVAL
    # =========================================================

    @staticmethod
    def mark_hospital_arrived(emergency_id):

        emergency = EmergencyRepository.get_by_id(
            emergency_id
        )

        if not emergency:
            return None, "Emergency request not found"

        if emergency.status != "Patient Picked Up":
            return None, (
                "Patient must be picked up before "
                "hospital arrival"
            )

        emergency.status = "Hospital Arrived"

        EmergencyRepository.update(emergency)

        return emergency, None

    # =========================================================
    # COMPLETE EMERGENCY
    # =========================================================

    @staticmethod
    def complete_emergency(emergency_id):

        emergency = EmergencyRepository.get_by_id(
            emergency_id
        )

        if not emergency:
            return None, "Emergency request not found"

        if emergency.status != "Hospital Arrived":
            return None, (
                "Emergency can only be completed "
                "after hospital arrival"
            )

        emergency.status = "Completed"

        # Release ambulance
        if emergency.ambulance_id:

            ambulance = Ambulance.query.get(
                emergency.ambulance_id
            )

            if ambulance:

                ambulance.availability_status = "Available"
                ambulance.emergency_status = "Normal"

        EmergencyRepository.update(emergency)

        return emergency, None

    # =========================================================
    # CANCEL EMERGENCY
    # =========================================================

    @staticmethod
    def cancel_emergency(emergency_id):

        emergency = EmergencyRepository.get_by_id(
            emergency_id
        )

        if not emergency:
            return None, "Emergency request not found"

        if emergency.status in [
            "Completed",
            "Cancelled"
        ]:
            return None, (
                f"Emergency is already {emergency.status.lower()}"
            )

        emergency.status = "Cancelled"

        # Release assigned ambulance
        if emergency.ambulance_id:

            ambulance = Ambulance.query.get(
                emergency.ambulance_id
            )

            if ambulance:

                ambulance.availability_status = "Available"
                ambulance.emergency_status = "Normal"

        EmergencyRepository.update(emergency)

        return emergency, None