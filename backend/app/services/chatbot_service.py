# =========================================================
# MEDILINK CHATBOT SERVICE
# =========================================================

import uuid


class ChatbotService:
    """
    Service layer for the MediLink AI Assistant.

    This first version provides a reliable rule-based
    assistant. The AI/LLM integration can be added later
    without changing the chatbot route structure.
    """

    # =====================================================
    # MAIN CHAT METHOD
    # =====================================================

    @staticmethod
    def chat(message, conversation_id=None):

        # -------------------------------------------------
        # Conversation ID
        # -------------------------------------------------

        if not conversation_id:

            conversation_id = str(
                uuid.uuid4()
            )

        # -------------------------------------------------
        # Normalize message
        # -------------------------------------------------

        original_message = message.strip()

        normalized_message = (
            original_message
            .lower()
        )

        # =================================================
        # GREETINGS
        # =================================================

        greeting_words = [
            "hello",
            "hi",
            "hey",
            "good morning",
            "good afternoon",
            "good evening"
        ]

        if any(
            word in normalized_message
            for word in greeting_words
        ):

            return {
                "message": (
                    "Hello! 👋 Welcome to MediLink. "
                    "I'm your MediLink Assistant. "
                    "I can help you with appointments, "
                    "doctors, hospitals, payments, "
                    "medical records and other "
                    "MediLink services."
                ),

                "conversation_id": conversation_id,

                "suggestions": [
                    "How do I book an appointment?",
                    "Show me the available doctors",
                    "How can I find hospitals?"
                ],

                "type": "greeting"
            }

        # =================================================
        # APPOINTMENT HELP
        # =================================================

        appointment_keywords = [
            "appointment",
            "book appointment",
            "schedule appointment",
            "booking appointment",
            "appointment booking"
        ]

        if any(
            keyword in normalized_message
            for keyword in appointment_keywords
        ):

            return {
                "message": (
                    "You can book an appointment through "
                    "MediLink by selecting a hospital, "
                    "doctor, appointment date and available "
                    "time slot. You can also choose "
                    "Online or Offline consultation."
                ),

                "conversation_id": conversation_id,

                "suggestions": [
                    "How do I cancel an appointment?",
                    "How do I find a doctor?",
                    "What is online consultation?"
                ],

                "type": "appointment"
            }

        # =================================================
        # CANCEL APPOINTMENT
        # =================================================

        cancellation_keywords = [
            "cancel appointment",
            "cancel my appointment",
            "appointment cancellation"
        ]

        if any(
            keyword in normalized_message
            for keyword in cancellation_keywords
        ):

            return {
                "message": (
                    "To cancel an appointment, open your "
                    "appointments section, select the "
                    "appointment and choose the cancellation "
                    "option. The final cancellation and "
                    "refund status may depend on the "
                    "appointment and payment status."
                ),

                "conversation_id": conversation_id,

                "suggestions": [
                    "How do I book an appointment?",
                    "How can I check my payments?"
                ],

                "type": "appointment_cancellation"
            }

        # =================================================
        # DOCTOR INFORMATION
        # =================================================

        doctor_keywords = [
            "doctor",
            "doctors",
            "find doctor",
            "available doctor",
            "available doctors",
            "specialist",
            "specialization"
        ]

        if any(
            keyword in normalized_message
            for keyword in doctor_keywords
        ):

            return {
                "message": (
                    "MediLink allows users to find doctors "
                    "by hospital and specialization. "
                    "Doctor profiles can include their "
                    "qualification, experience, consultation "
                    "fee and availability."
                ),

                "conversation_id": conversation_id,

                "suggestions": [
                    "How do I book an appointment?",
                    "How do I find a hospital?",
                    "What is a doctor's schedule?"
                ],

                "type": "doctor"
            }

        # =================================================
        # HOSPITAL INFORMATION
        # =================================================

        hospital_keywords = [
            "hospital",
            "hospitals",
            "find hospital",
            "available hospital",
            "hospital availability"
        ]

        if any(
            keyword in normalized_message
            for keyword in hospital_keywords
        ):

            return {
                "message": (
                    "MediLink provides hospital information "
                    "through its hospital management module. "
                    "Users can view registered hospitals and "
                    "use hospital information while selecting "
                    "doctors and appointments."
                ),

                "conversation_id": conversation_id,

                "suggestions": [
                    "Show me doctors",
                    "How do I book an appointment?",
                    "How does MediLink work?"
                ],

                "type": "hospital"
            }

        # =================================================
        # PAYMENT INFORMATION
        # =================================================

        payment_keywords = [
            "payment",
            "payments",
            "pay",
            "bill",
            "billing",
            "transaction",
            "refund"
        ]

        if any(
            keyword in normalized_message
            for keyword in payment_keywords
        ):

            return {
                "message": (
                    "MediLink includes billing and payment "
                    "management. Payments are associated "
                    "with bills and can contain payment "
                    "method, transaction information, "
                    "payment status and payment date."
                ),

                "conversation_id": conversation_id,

                "suggestions": [
                    "How can I check my bill?",
                    "How can I check my payment status?",
                    "How do I book an appointment?"
                ],

                "type": "payment"
            }

        # =================================================
        # MEDICAL RECORDS
        # =================================================

        medical_record_keywords = [
            "medical record",
            "medical records",
            "health record",
            "health records",
            "medical history",
            "my records"
        ]

        if any(
            keyword in normalized_message
            for keyword in medical_record_keywords
        ):

            return {
                "message": (
                    "MediLink provides a medical-record "
                    "module where authorized users can "
                    "manage patient medical information "
                    "and records."
                ),

                "conversation_id": conversation_id,

                "suggestions": [
                    "How do I find my prescriptions?",
                    "How do I book an appointment?",
                    "How does MediLink protect my information?"
                ],

                "type": "medical_record"
            }

        # =================================================
        # PRESCRIPTION
        # =================================================

        prescription_keywords = [
            "prescription",
            "prescriptions",
            "medicine",
            "medicines"
        ]

        if any(
            keyword in normalized_message
            for keyword in prescription_keywords
        ):

            return {
                "message": (
                    "MediLink includes prescription and "
                    "medicine management features. "
                    "Prescription information should be "
                    "used according to instructions from "
                    "a qualified healthcare professional."
                ),

                "conversation_id": conversation_id,

                "suggestions": [
                    "How do I view my medical records?",
                    "How do I find a doctor?",
                    "How do I book an appointment?"
                ],

                "type": "prescription"
            }

        # =================================================
        # LABORATORY
        # =================================================

        laboratory_keywords = [
            "laboratory",
            "lab",
            "lab test",
            "lab tests",
            "test report",
            "test reports"
        ]

        if any(
            keyword in normalized_message
            for keyword in laboratory_keywords
        ):

            return {
                "message": (
                    "MediLink includes laboratory test "
                    "management. Laboratory information can "
                    "be associated with patients and doctors "
                    "within the system."
                ),

                "conversation_id": conversation_id,

                "suggestions": [
                    "How do I view medical records?",
                    "How do I find a doctor?",
                    "How do I book an appointment?"
                ],

                "type": "laboratory"
            }

        # =================================================
        # MEDICINE / PHARMACY
        # =================================================

        medicine_keywords = [
            "medicine stock",
            "medicine inventory",
            "pharmacy",
            "low stock",
            "available medicine"
        ]

        if any(
            keyword in normalized_message
            for keyword in medicine_keywords
        ):

            return {
                "message": (
                    "MediLink includes medicine inventory "
                    "management. Authorized users can manage "
                    "medicine information and monitor "
                    "low-stock medicines."
                ),

                "conversation_id": conversation_id,

                "suggestions": [
                    "What is low stock?",
                    "How do prescriptions work?",
                    "How do I find a doctor?"
                ],

                "type": "medicine"
            }

        # =================================================
        # AI / ASSISTANT INFORMATION
        # =================================================

        assistant_keywords = [
            "what can you do",
            "what do you do",
            "help",
            "features",
            "what can i ask"
        ]

        if any(
            keyword in normalized_message
            for keyword in assistant_keywords
        ):

            return {
                "message": (
                    "I'm the MediLink Assistant. 🤖 "
                    "I can help explain MediLink features "
                    "such as appointments, doctors, hospitals, "
                    "payments, bills, prescriptions, laboratory "
                    "services and medical records."
                ),

                "conversation_id": conversation_id,

                "suggestions": [
                    "How do I book an appointment?",
                    "Show me information about doctors",
                    "How do payments work?"
                ],

                "type": "assistant_help"
            }

        # =================================================
        # MEDICAL SAFETY
        # =================================================

        medical_keywords = [
            "symptom",
            "symptoms",
            "disease",
            "diagnose",
            "diagnosis",
            "treatment",
            "pain",
            "fever",
            "medicine for",
            "what medicine should"
        ]

        if any(
            keyword in normalized_message
            for keyword in medical_keywords
        ):

            return {
                "message": (
                    "I can provide general information, "
                    "but I cannot diagnose medical conditions "
                    "or prescribe treatment. For personal "
                    "medical advice, please consult a qualified "
                    "healthcare professional."
                ),

                "conversation_id": conversation_id,

                "suggestions": [
                    "How do I find a doctor?",
                    "How do I book an appointment?",
                    "How do I view my medical records?"
                ],

                "type": "medical_safety"
            }

        # =================================================
        # ABOUT MEDILINK
        # =================================================

        medilink_keywords = [
            "what is medilink",
            "about medilink",
            "tell me about medilink",
            "medilink"
        ]

        if any(
            keyword in normalized_message
            for keyword in medilink_keywords
        ):

            return {
                "message": (
                    "MediLink is a smart hospital management "
                    "platform designed to connect patients, "
                    "doctors, hospitals and healthcare-related "
                    "services through a centralized digital "
                    "system."
                ),

                "conversation_id": conversation_id,

                "suggestions": [
                    "What can MediLink do?",
                    "How do I book an appointment?",
                    "How can I find a doctor?"
                ],

                "type": "about"
            }

        # =================================================
        # DEFAULT RESPONSE
        # =================================================

        return {
            "message": (
                "I'm not sure I understood that. "
                "I can help you with MediLink features "
                "such as appointments, doctors, hospitals, "
                "payments, bills, prescriptions, laboratory "
                "services and medical records."
            ),

            "conversation_id": conversation_id,

            "suggestions": [
                "How do I book an appointment?",
                "How do I find a doctor?",
                "How do payments work?"
            ],

            "type": "general"
        }