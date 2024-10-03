from django.db import models

from notification.domain.notification import NotificationType
from notification.infra.models import Notification
from user.infra.models.user import User


class UserNotificationSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_constraint=False)
    receive_system_notifications = models.BooleanField(default=True)
    receive_advertisement_notifications = models.BooleanField(default=True)
    receive_friend_request_notifications = models.BooleanField(default=True)
    receive_sent_letter_notifications = models.BooleanField(default=True)
    receive_arrival_notifications = models.BooleanField(default=True)

    def update_setting(self, notification_type: str, enabled: bool):
        if notification_type == NotificationType.SYSTEM:
            self.receive_system_notifications = enabled
        elif notification_type == NotificationType.ADVERTISEMENT:
            self.receive_advertisement_notifications = enabled
        elif notification_type == NotificationType.FRIEND_REQUEST:
            self.receive_friend_request_notifications = enabled
        elif notification_type == NotificationType.SENT_LETTER:
            self.receive_sent_letter_notifications = enabled
        elif notification_type == NotificationType.ARRIVAL:
            self.receive_arrival_notifications = enabled
        self.save()

    class Meta:
        db_table = "UserNotificationSetting"


class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    notification = models.ForeignKey(
        Notification, on_delete=models.CASCADE, db_constraint=False
    )
    is_read = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    class Meta:
        db_table = "UserNotification"
