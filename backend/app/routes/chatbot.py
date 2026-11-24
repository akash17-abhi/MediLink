# =========================================================
# MEDILINK CHATBOT ROUTES
# =========================================================

from flask import Blueprint, request

from app.schemas.chatbot_schema import (
    validate_chatbot_message,
    chatbot_response_to_dict
)

from app.services.chatbot_service import (
    ChatbotService
)


# =========================================================
# BLUEPRINT
# =========================================================

chatbot_bp = Blueprint(
    "chatbot",
    __name__,
    url_prefix="/api/chatbot"
)


# =========================================================
# CHAT WITH MEDILINK ASSISTANT
# =========================================================

@chatbot_bp.post("/chat")
def chat():

    # -----------------------------------------------------
    # Get request body
    # -----------------------------------------------------

    data = request.get_json(
        silent=True
    ) or {}

    # -----------------------------------------------------
    # Validate request
    # -----------------------------------------------------

    valid, message = validate_chatbot_message(
        data
    )

    if not valid:

        return {
            "success": False,
            "message": message
        }, 400

    # -----------------------------------------------------
    # Get message
    # -----------------------------------------------------

    user_message = data["message"].strip()

    conversation_id = data.get(
        "conversation_id"
    )

    # -----------------------------------------------------
    # Generate chatbot response
    # -----------------------------------------------------

    response = ChatbotService.chat(
        message=user_message,
        conversation_id=conversation_id
    )

    # -----------------------------------------------------
    # Return response
    # -----------------------------------------------------

    return {
        "success": True,
        "response": chatbot_response_to_dict(
            response
        )
    }, 200


# =========================================================
# CHATBOT HEALTH CHECK
# =========================================================

@chatbot_bp.get("/health")
def health():

    return {
        "success": True,
        "message": "MediLink Assistant is working"
    }, 200