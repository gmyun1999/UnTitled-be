from common.infra.serializer import DynamicFieldsModelSerializer
from lucky_letter.infra.models.letter_model import Envelope, Letter, Stamp, WritingPad


class WritingPadSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = WritingPad
        fields = "__all__"


class EnvelopeSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Envelope
        fields = "__all__"


class StampSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Stamp
        fields = "__all__"


class LetterSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Letter
        fields = "__all__"
