from app import db

from app.models.notification import Notification
from app.repositories.notification_repository import NotificationRepository


class NotificationService:
    """Service layer for Notification operations"""

    repo = NotificationRepository()

    @staticmethod
    def create(data):
        """Create a new notification"""

        notification = Notification(
            user_id=data["user_id"],
            title=data["title"],
            message=data["message"],
            notification_type=data["notification_type"],
            is_read=data.get("is_read", False)
        )

        return NotificationService.repo.create(notification)

    @staticmethod
    def get_all():
        """Get all notifications"""

        return NotificationService.repo.get_all()

    @staticmethod
    def get_by_id(notification_id):
        """Get notification by ID"""

        return NotificationService.repo.get_by_id(notification_id)

    @staticmethod
    def get_by_user_id(user_id):
        """Get all notifications for a specific user"""

        return NotificationService.repo.get_by_user_id(user_id)

    @staticmethod
    def get_unread_by_user_id(user_id):
        """Get unread notifications for a specific user"""

        return NotificationService.repo.get_unread_by_user_id(user_id)

    @staticmethod
    def get_unread_count(user_id):
        """Get unread notification count"""

        return NotificationService.repo.get_unread_count(user_id)

    @staticmethod
    def mark_as_read(notification_id):
        """Mark a notification as read"""

        return NotificationService.repo.mark_as_read(notification_id)

    @staticmethod
    def mark_all_as_read(user_id):
        """Mark all notifications of a user as read"""

        return NotificationService.repo.mark_all_as_read(user_id)

    @staticmethod
    def update(notification_id, data):
        """Update a notification"""

        notification = NotificationService.repo.get_by_id(
            notification_id
        )

        if not notification:
            return None

        allowed_fields = [
            "title",
            "message",
            "notification_type",
            "is_read"
        ]

        for key, value in data.items():
            if key in allowed_fields:
                setattr(notification, key, value)

        return NotificationService.repo.update(notification)

    @staticmethod
    def delete(notification_id):
        """Delete a notification"""

        notification = NotificationService.repo.get_by_id(
            notification_id
        )

        if not notification:
            return False

        return NotificationService.repo.delete(notification)

    @staticmethod
    def delete_by_user_id(user_id):
        """Delete all notifications belonging to a user"""

        return NotificationService.repo.delete_by_user_id(user_id)