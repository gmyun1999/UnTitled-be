from rest_framework import serializers

from lucky_letter.domain.letter import FontType


class LetterBodyRequestSerializer(serializers.Serializer):
    to_app_id = serializers.CharField(max_length=36)
    to_letter_id = serializers.CharField(
        max_length=36, allow_null=True, required=False
    )  # 답장이 아닌 경우 None
    is_anonymous = serializers.BooleanField(default=False)
    writing_pad_id = serializers.CharField(max_length=36)
    envelope_id = serializers.CharField(max_length=36)
    stamp_id = serializers.CharField(max_length=36)
    content = serializers.CharField(max_length=1000)
    title = serializers.CharField(max_length=50)
    font = serializers.ChoiceField(
        choices=[(font.name, font.value) for font in FontType]
    )  # FontType Enum 사용
    will_arrive_at = serializers.CharField(allow_null=True, required=False)  # None 허용


class LetterStandardResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = LetterBodyRequestSerializer()
    http_status = serializers.IntegerField()
