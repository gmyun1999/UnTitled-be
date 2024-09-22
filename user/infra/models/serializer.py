from common.infra.serializer import (
    DynamicFieldsModelSerializer,
    DynamicNestedFieldSerializer,
)
from user.domain.user import UserRelation as UserRelationVo
from user.infra.models.user import User, UserRelation


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
