from rest_framework import serializers


class UserResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    app_id = serializers.CharField()
    name = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class WritingPadResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    url = serializers.URLField()


class EnvelopeResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    url = serializers.URLField()


class StampResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    url = serializers.URLField()


class LetterResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    from_user_id = UserResponseSerializer()
    to_user_id = UserResponseSerializer()
    writing_pad_id = WritingPadResponseSerializer()
    envelope_id = EnvelopeResponseSerializer()
    stamp_id = StampResponseSerializer()
    is_anonymous = serializers.BooleanField()
    content = serializers.CharField()
    title = serializers.CharField()
    font = serializers.CharField()
    will_arrive_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class LetterBoxResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    letter_id = LetterResponseSerializer()
    type = serializers.CharField()
    is_read = serializers.BooleanField()
    delivered_at = serializers.DateTimeField()
    user_id = serializers.UUIDField()


class LetterBoxListResponseSerializer(serializers.ListSerializer):
    child = LetterBoxResponseSerializer()


class LetterBoxListStandardResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = LetterBoxListResponseSerializer()
    http_status = serializers.IntegerField()


class LetterBoxStandardResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = LetterBoxResponseSerializer()
    http_status = serializers.IntegerField()


class LetterStandardResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = LetterResponseSerializer()
    http_status = serializers.IntegerField()
