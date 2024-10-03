from common.infra.serializer import (
    DynamicFieldsModelSerializer,
    DynamicNestedFieldSerializer,
)
from lucky_letter.infra.models.serializers import LetterSerializer
from user.domain.user import UserRelation as UserRelationVo
from user.domain.user_letter_box import UserLetterBox as UserLetterBoxVo
from user.infra.models.user import User, UserLetterBox, UserRelation


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


class NestedUserLetterBoxSerializer(DynamicFieldsModelSerializer):
    letter_id = LetterSerializer()

    class Meta:
        model = UserLetterBox
        fields = "__all__"
        nested_serializers = {
            UserLetterBoxVo.FIELD_USER_ID: UserSerializer,
            UserLetterBoxVo.FIELD_LETTER_ID: LetterSerializer,
        }
