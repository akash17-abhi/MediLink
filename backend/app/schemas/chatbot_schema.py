# =========================================================
# MEDILINK CHATBOT SCHEMA
# =========================================================


def validate_chatbot_message(data):
    """
    Validate incoming chatbot requests.
    """

    # -----------------------------------------------------
    # Request body validation
    # -----------------------------------------------------

    if not data:
        return False, "Request body is required"

    # -----------------------------------------------------
    # Message validation
    # -----------------------------------------------------

    if "message" not in data:
        return False, "message is required"

    message = data.get("message")

    if message is None:
        return False, "message is required"

    if not isinstance(message, str):
        return False, "message must be a string"

    message = message.strip()

    if not message:
        return False, "message cannot be empty"

    # -----------------------------------------------------
    # Message length validation
    # -----------------------------------------------------

    if len(message) > 2000:
        return (
            False,
            "message cannot exceed 2000 characters"
        )

    # -----------------------------------------------------
    # Optional conversation ID
    # -----------------------------------------------------

    if data.get("conversation_id") is not None:

        conversation_id = data.get(
            "conversation_id"
        )

        if not isinstance(
            conversation_id,
            str
        ):

            return (
                False,
                "conversation_id must be a string"
            )

    # -----------------------------------------------------
    # Validation successful
    # -----------------------------------------------------

    return True, ""


# =========================================================
# CHATBOT RESPONSE → DICTIONARY
# =========================================================


def chatbot_response_to_dict(
    response
):
    """
    Convert chatbot response into
    a consistent API response structure.
    """

    return {
        "message": response.get(
            "message",
            ""
        ),

        "conversation_id": response.get(
            "conversation_id"
        ),

        "suggestions": response.get(
            "suggestions",
            []
        ),

        "type": response.get(
            "type",
            "general"
        )
    }