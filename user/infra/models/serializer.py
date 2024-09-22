from rest_framework import serializers

from user.infra.models.user import User, UserRelation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRelation
        fields = "__all__"
