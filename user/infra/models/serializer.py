from common.infra.serializer import (
    DynamicFieldsModelSerializer,
    DynamicNestedFieldSerializer,
)
from user.domain.user import UserRelation as UserRelationVo
from user.infra.models.notification_model import (
    UserNotification,
    UserNotificationSetting,
)
from user.infra.models.user_letter_box_model import UserLetterBox
from user.infra.models.user_model import User, UserPushToken, UserRelation


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserRelationSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = UserRelation
        fields = "__all__"


class UserJoinRelationSerializer(DynamicNestedFieldSerializer):
    class Meta:
        model = UserRelation
        fields = "__all__"
        nested_serializers = {
            UserRelationVo.FIELD_TO_ID: UserSerializer,
            UserRelationVo.FIELD_FROM_ID: UserSerializer,
        }


class UserLetterBoxSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = UserLetterBox
        fields = "__all__"


class UserNotificationSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = UserNotification
        fields = "__all__"


class UserNotificationSettingSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = UserNotificationSetting
        fields = "__all__"


class UserPushTokenSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = UserPushToken
        fields = "__all__"
