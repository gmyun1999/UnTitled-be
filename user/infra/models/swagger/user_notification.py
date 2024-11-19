from rest_framework import serializers

from notification.domain.notification import NotificationType


class GetUserNotificationSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=36)
    user_id = serializers.CharField(max_length=36)
    notification_id = serializers.CharField(max_length=36)
    is_read = serializers.BooleanField()
    delivered_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class GetNotificationSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=36)
    title = serializers.CharField(max_length=255)
    message = serializers.CharField()
    notification_type = serializers.CharField(max_length=50)
    created_at = serializers.DateTimeField()
    is_system_wide = serializers.BooleanField()
    related_domain = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    related_object_id = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )


class GetNestedUserNotificationSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=36)
    user_id = serializers.CharField(max_length=36)
    is_read = serializers.BooleanField()
    delivered_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    notification_id = GetNotificationSerializer()


class GetNestedPagingUserNotificationSerializer(serializers.Serializer):
    items = GetNestedUserNotificationSerializer(many=True)
    total_items = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    current_page = serializers.IntegerField()
    page_size = serializers.IntegerField()
    has_previous = serializers.BooleanField()
    has_next = serializers.BooleanField()


class PutNotificationBodyRequestSerializer(serializers.Serializer):
    is_read = serializers.BooleanField()


class GetUserNotificationSettingSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=36)
    user_id = serializers.CharField(max_length=36)
    notification_type = serializers.CharField(max_length=20)
    is_push_allow = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class GetAllUserNotificationSettingSerializer(serializers.Serializer):
    settings = GetUserNotificationSettingSerializer(many=True)


class PutUserNotificationSettingSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=36)
    user_id = serializers.CharField(max_length=36)
    notification_type = serializers.CharField(max_length=20)
    is_push_allow = serializers.BooleanField()
