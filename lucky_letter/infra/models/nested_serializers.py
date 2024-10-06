from rest_framework import serializers

from common.infra.serializer import DynamicFieldsModelSerializer
from lucky_letter.domain.letter import Letter as LetterVo
from lucky_letter.infra.models.letter_model import Letter
from lucky_letter.infra.models.serializers import (
    EnvelopeSerializer,
    StampSerializer,
    WritingPadSerializer,
)
from user.infra.models.serializer import UserSerializer


class NestedLetterSerializer(serializers.ModelSerializer):
    from_user_id = UserSerializer()
    to_user_id = UserSerializer()
    writing_pad_id = WritingPadSerializer()
    envelope_id = EnvelopeSerializer()
    stamp_id = StampSerializer()

    class Meta:
        model = Letter
        fields = "__all__"
        nested_serializers = {
            LetterVo.FIELD_FROM_USER_ID: UserSerializer,
            LetterVo.FIELD_TO_USER_ID: UserSerializer,
            LetterVo.FIELD_ENVELOPE_ID: EnvelopeSerializer,
            LetterVo.FIELD_STAMP_ID: StampSerializer,
            LetterVo.FIELD_WRITING_PAD_ID: WritingPadSerializer,
        }
