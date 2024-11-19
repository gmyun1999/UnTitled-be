from drf_spectacular.utils import extend_schema
from rest_framework import serializers

from user.domain.user import RelationStatus, RelationType


class UserRelationCreateRequestSerializer(serializers.Serializer):
    relation = serializers.ChoiceField(
        choices=[RelationType.FRIEND], help_text="관계 타입 (예: FRIEND)"
    )
    status = serializers.ChoiceField(
        choices=[RelationStatus.PENDING], help_text="관계 상태 (예: PENDING)"
    )
    to_app_id = serializers.CharField(max_length=16, help_text="대상 사용자의 앱 ID")


class UserRelationDeleteRequestSerializer(serializers.Serializer):
    relation = serializers.ChoiceField(
        choices=[RelationType.FRIEND], help_text="관계 타입 (예: FRIEND)"
    )
    to_app_id = serializers.CharField(max_length=16, help_text="대상 사용자의 앱 ID")


class UserRelationResponseSerializer(serializers.Serializer):
    id = serializers.CharField(help_text="관계 ID")
    to_id = serializers.CharField(help_text="대상 사용자 ID")
    from_id = serializers.CharField(help_text="요청한 사용자 ID")
    relation_type = serializers.ChoiceField(
        choices=[RelationType.FRIEND], help_text="관계 타입"
    )
    relation_status = serializers.ChoiceField(
        choices=[RelationStatus.PENDING, RelationStatus.REJECT, RelationStatus.ACCEPT],
        help_text="관계 상태",
    )
    created_at = serializers.DateTimeField(help_text="생성 일자")
    updated_at = serializers.DateTimeField(help_text="업데이트 일자")


class ErrorResponseSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="에러 메시지")
    http_status = serializers.IntegerField(help_text="HTTP 상태 코드")
