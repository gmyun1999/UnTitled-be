from django.db import models

from lucky_letter.infra.models.letter_model import Letter


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
        related_name="to_user_id",
        db_constraint=False,
        on_delete=models.SET_NULL,
        null=True,
    )
    from_id = models.ForeignKey(
        to=User,
        max_length=36,
        related_name="from_user_id",
        db_constraint=False,
        on_delete=models.SET_NULL,
        null=True,
    )
    relation_type = models.CharField(max_length=36)
    relation_status = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "UserRelation"


class UserLetterBox(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.ForeignKey(
        to=User,
        max_length=36,
        related_name="user_id",
        db_constraint=False,
        on_delete=models.SET_NULL,
        null=True,
    )
    letter_id = models.ForeignKey(
        to=Letter,
        max_length=36,
        related_name="letter_id",
        db_constraint=False,
        on_delete=models.SET_NULL,
        null=True,
    )
    type = models.CharField(max_length=10)
    is_read = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()
