from django.db import models


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    app_id = models.CharField(max_length=16, unique=True, null=True)
    name = models.CharField(max_length=64, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "User"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["app_id"]),
        ]


class UserRelation(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    to_id = models.ForeignKey(
        to=User,
        max_length=36,
        db_constraint=False,
        related_name="user_relation_to_id",
        on_delete=models.CASCADE,
        null=True,
    )
    from_id = models.ForeignKey(
        to=User,
        max_length=36,
        db_constraint=False,
        on_delete=models.CASCADE,
        related_name="user_relation_from_id",
        null=True,
    )
    relation_type = models.CharField(max_length=36)
    relation_status = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "UserRelation"


class UserPushToken(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.ForeignKey(
        to=User,
        max_length=36,
        db_constraint=False,
        on_delete=models.CASCADE,
        related_name="push_token_user",
    )
    token = models.CharField(max_length=4096)
    push_service = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
