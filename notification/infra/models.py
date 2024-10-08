from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Notification(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    is_system_wide = models.BooleanField(default=False)
    # 아무 모델이나 notification 이랑 관련있으면 들어갈수있음.
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        db_table = "Notification"
