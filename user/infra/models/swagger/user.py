from rest_framework import serializers


class DuplicateDateResponseSerializer(serializers.Serializer):
    target = serializers.CharField()
    is_duplicate = serializers.BooleanField()


class UserDuplicateCheckStandardResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = DuplicateDateResponseSerializer(many=True)
    http_status = serializers.IntegerField()


class ValidateBodyRequestSerializer(serializers.Serializer):
    app_id = serializers.CharField(max_length=16, allow_null=True, required=False)
    name = serializers.CharField(max_length=64, allow_null=True, required=False)


class CreateUserBodyRequestSerializer(serializers.Serializer):
    app_id = serializers.CharField(max_length=16, allow_null=True, required=False)
    name = serializers.CharField(max_length=64, allow_null=True, required=False)


class UserCreateStandardResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = serializers.CharField()
    http_status = serializers.IntegerField()
