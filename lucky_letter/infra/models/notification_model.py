from django.db import models


class NotificationSetting(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    type = models.CharField(max_length=36)
    user_id = models.CharField(max_length=36)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "NotificationSetting"
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
        ]


class Notification(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    sender_id = models.CharField(max_length=36)
    receiver_id = models.CharField(max_length=36)
    type = models.CharField(max_length=36)
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Notification"
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
        ]

    def __str__(self):
        return self.title
