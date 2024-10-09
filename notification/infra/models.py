from django.db import models


class Notification(models.Model):
    FIELD_CONTENT_TYPE = "content_type"
    FIELD_OBJECT_ID = "object_id"

    id = models.CharField(primary_key=True, max_length=36)
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    is_system_wide = models.BooleanField(default=False)

    # 아무 모델 id나 notification 이랑 관련있으면 들어갈수있음.
    related_domain = models.CharField(max_length=100, null=True, blank=True)
    related_object_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "Notification"
