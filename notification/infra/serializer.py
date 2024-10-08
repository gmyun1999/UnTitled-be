from common.infra.serializer import DynamicFieldsModelSerializer
from notification.infra.models import Notification


class NotificationSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
