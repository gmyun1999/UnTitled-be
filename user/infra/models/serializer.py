from common.infra.serializer import (
    DynamicFieldsModelSerializer,
    DynamicNestedFieldSerializer,
)
from user.domain.user import UserRelation as UserRelationVo
from user.infra.models.user import User, UserRelation
from user.infra.models.user_letter_box_model import UserLetterBox


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
