from app.models.notification import Notification
from app import db


class NotificationRepository:
    """Repository for Notification operations"""

    def create(self, notification):
        """Create a new notification"""
        db.session.add(notification)
        db.session.commit()
        return notification

    def get_all(self):
        """Get all notifications"""
        return Notification.query.order_by(
            Notification.created_at.desc()
        ).all()

    def get_by_id(self, notification_id):
        """Get notification by ID"""
        return Notification.query.get(notification_id)

    def get_by_user_id(self, user_id):
        """Get all notifications for a specific user"""
        return Notification.query.filter_by(
            user_id=user_id
        ).order_by(
            Notification.created_at.desc()
        ).all()

    def get_unread_by_user_id(self, user_id):
        """Get unread notifications for a user"""
        return Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).order_by(
            Notification.created_at.desc()
        ).all()

    def get_unread_count(self, user_id):
        """Get unread notification count"""
        return Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).count()

    def mark_as_read(self, notification_id):
        """Mark a notification as read"""
        notification = self.get_by_id(notification_id)

        if not notification:
            return None

        notification.is_read = True
        db.session.commit()

        return notification

    def mark_all_as_read(self, user_id):
        """Mark all notifications of a user as read"""

        notifications = Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).all()

        for notification in notifications:
            notification.is_read = True

        db.session.commit()

        return len(notifications)

    def update(self, notification):
        """Update notification"""
        db.session.commit()
        return notification

    def delete(self, notification):
        """Delete notification"""
        db.session.delete(notification)
        db.session.commit()
        return True

    def delete_by_user_id(self, user_id):
        """Delete all notifications of a user"""

        notifications = Notification.query.filter_by(
            user_id=user_id
        ).all()

        for notification in notifications:
            db.session.delete(notification)

        db.session.commit()

        return len(notifications)