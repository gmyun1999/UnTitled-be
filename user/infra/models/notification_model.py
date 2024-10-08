from django.db import models

from notification.infra.models import Notification
from user.infra.models.user_model import User


class UserNotificationSetting(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    notification_type = models.CharField(max_length=20)
    is_push_allow = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "UserNotificationSetting"


class UserNotification(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    notification_id = models.ForeignKey(
        Notification, on_delete=models.CASCADE, db_constraint=False
    )
    is_read = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    class Meta:
        db_table = "UserNotification"
