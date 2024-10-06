from rest_framework import serializers

from common.infra.serializer import DynamicFieldsModelSerializer
from lucky_letter.infra.models.nested_serializers import NestedLetterSerializer
from lucky_letter.infra.models.serializers import LetterSerializer
from user.domain.user_letter_box import UserLetterBox as UserLetterBoxVo
from user.infra.models.user_letter_box_model import UserLetterBox


class NestedUserLetterBoxSerializer(serializers.ModelSerializer):
    letter_id = NestedLetterSerializer()

    class Meta:
        model = UserLetterBox
        fields = "__all__"
        nested_serializers = {UserLetterBoxVo.FIELD_LETTER_ID: NestedLetterSerializer}
