from rest_framework import serializers

from common.infra.serializer import DynamicFieldsModelSerializer
from lucky_letter.infra.models.nested_serializers import NestedLetterSerializer
from lucky_letter.infra.models.serializers import LetterSerializer
from notification.infra.serializer import NotificationSerializer
from user.domain.user_letter_box import UserLetterBox as UserLetterBoxVo
from user.domain.user_notification import UserNotification as UserNotificationVo
from user.infra.models.notification_model import UserNotification
from user.infra.models.user_letter_box_model import UserLetterBox


class NestedUserLetterBoxSerializer(serializers.ModelSerializer):
    letter_id = NestedLetterSerializer()

    class Meta:
        model = UserLetterBox
        fields = "__all__"
        nested_serializers = {UserLetterBoxVo.FIELD_LETTER_ID: NestedLetterSerializer}


class NestedUserNotificationSerializer(DynamicFieldsModelSerializer):
    notification_id = NotificationSerializer()

    class Meta:
        model = UserNotification
        fields = "__all__"
        nested_serializers = {
            UserNotificationVo.FIELD_NOTIFICATION_ID: NotificationSerializer
        }
