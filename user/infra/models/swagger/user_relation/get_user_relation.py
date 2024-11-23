from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    email = serializers.EmailField()


class UserRelationItemSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    relation_type = serializers.CharField()
    relation_status = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    to_id = UserSerializer()
    from_id = UserSerializer()


class UserRelationDataSerializer(serializers.Serializer):
    items = UserRelationItemSerializer(many=True)
    total_items = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    current_page = serializers.IntegerField()
    page_size = serializers.IntegerField()
    has_previous = serializers.BooleanField()
    has_next = serializers.BooleanField()


class UserRelationResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = UserRelationDataSerializer()
    http_status = serializers.IntegerField()


class GetUserRelationResponseSerializer(serializers.Serializer):
    data = UserRelationItemSerializer()
    message = serializers.CharField()
    http_status = serializers.IntegerField()
