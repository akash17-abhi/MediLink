from flask import Blueprint, request

from app.schemas.notification_schema import (
    validate_notification,
    notification_to_dict
)

from app.services.notification_service import NotificationService


notification_bp = Blueprint(
    "notification",
    __name__,
    url_prefix="/api/notifications"
)


@notification_bp.post("/")
def create_notification():
    """Create a new notification"""

    data = request.get_json()

    valid, message = validate_notification(data)

    if not valid:
        return {
            "success": False,
            "message": message
        }, 400

    notification = NotificationService.create(data)

    return {
        "success": True,
        "message": "Notification created successfully",
        "notification": notification_to_dict(notification)
    }, 201


@notification_bp.get("/")
def get_all_notifications():
    """Get all notifications"""

    notifications = NotificationService.get_all()

    return {
        "success": True,
        "count": len(notifications),
        "notifications": [
            notification_to_dict(notification)
            for notification in notifications
        ]
    }, 200


@notification_bp.get("/<int:notification_id>")
def get_notification(notification_id):
    """Get notification by ID"""

    notification = NotificationService.get_by_id(
        notification_id
    )

    if not notification:
        return {
            "success": False,
            "message": "Notification not found"
        }, 404

    return {
        "success": True,
        "notification": notification_to_dict(notification)
    }, 200


@notification_bp.get("/user/<int:user_id>")
def get_user_notifications(user_id):
    """Get all notifications for a user"""

    notifications = NotificationService.get_by_user_id(
        user_id
    )

    return {
        "success": True,
        "count": len(notifications),
        "notifications": [
            notification_to_dict(notification)
            for notification in notifications
        ]
    }, 200


@notification_bp.get("/user/<int:user_id>/unread")
def get_unread_notifications(user_id):
    """Get unread notifications for a user"""

    notifications = NotificationService.get_unread_by_user_id(
        user_id
    )

    return {
        "success": True,
        "count": len(notifications),
        "notifications": [
            notification_to_dict(notification)
            for notification in notifications
        ]
    }, 200


@notification_bp.get("/user/<int:user_id>/unread/count")
def get_unread_count(user_id):
    """Get unread notification count"""

    count = NotificationService.get_unread_count(
        user_id
    )

    return {
        "success": True,
        "user_id": user_id,
        "unread_count": count
    }, 200


@notification_bp.patch("/<int:notification_id>/read")
def mark_as_read(notification_id):
    """Mark a notification as read"""

    notification = NotificationService.mark_as_read(
        notification_id
    )

    if not notification:
        return {
            "success": False,
            "message": "Notification not found"
        }, 404

    return {
        "success": True,
        "message": "Notification marked as read",
        "notification": notification_to_dict(notification)
    }, 200


@notification_bp.patch("/user/<int:user_id>/read-all")
def mark_all_as_read(user_id):
    """Mark all notifications of a user as read"""

    count = NotificationService.mark_all_as_read(
        user_id
    )

    return {
        "success": True,
        "message": "All notifications marked as read",
        "updated_count": count
    }, 200


@notification_bp.put("/<int:notification_id>")
def update_notification(notification_id):
    """Update a notification"""

    data = request.get_json()

    notification = NotificationService.update(
        notification_id,
        data
    )

    if not notification:
        return {
            "success": False,
            "message": "Notification not found"
        }, 404

    return {
        "success": True,
        "message": "Notification updated successfully",
        "notification": notification_to_dict(notification)
    }, 200


@notification_bp.delete("/<int:notification_id>")
def delete_notification(notification_id):
    """Delete a notification"""

    deleted = NotificationService.delete(
        notification_id
    )

    if not deleted:
        return {
            "success": False,
            "message": "Notification not found"
        }, 404

    return {
        "success": True,
        "message": "Notification deleted successfully"
    }, 200


@notification_bp.delete("/user/<int:user_id>")
def delete_user_notifications(user_id):
    """Delete all notifications for a user"""

    count = NotificationService.delete_by_user_id(
        user_id
    )

    return {
        "success": True,
        "message": "User notifications deleted successfully",
        "deleted_count": count
    }, 200