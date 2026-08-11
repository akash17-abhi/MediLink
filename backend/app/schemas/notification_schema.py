def validate_notification(data):
    """Validate notification data"""

    if not data:
        return False, "Request body is required"

    required_fields = [
        "user_id",
        "title",
        "message",
        "notification_type"
    ]

    for field in required_fields:
        if field not in data or data[field] in (None, ""):
            return False, f"{field} is required"

    if not isinstance(data["user_id"], int):
        return False, "user_id must be an integer"

    return True, ""


def notification_to_dict(notification):
    """Convert notification object to dictionary"""

    return {
        "id": notification.id,
        "user_id": notification.user_id,
        "title": notification.title,
        "message": notification.message,
        "notification_type": notification.notification_type,
        "is_read": notification.is_read,
        "created_at": (
            notification.created_at.strftime("%Y-%m-%d %H:%M:%S")
            if notification.created_at
            else None
        ),
        "updated_at": (
            notification.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            if notification.updated_at
            else None
        )
    }