from django.db import models

from user.infra.models.user import User


class WritingPad(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    name = models.CharField(max_length=255)
    url = models.URLField()

    class Meta:
        db_table = "WritingPad"

    def __str__(self):
        return self.name


class Envelope(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    name = models.CharField(max_length=255)
    url = models.URLField()

    class Meta:
        db_table = "Envelope"

    def __str__(self):
        return self.name


class Stamp(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    name = models.CharField(max_length=255)
    url = models.URLField()

    class Meta:
        db_table = "Stamp"

    def __str__(self):
        return self.name


class Letter(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    to_user_id = models.ForeignKey(
        User,
        default=None,
        db_constraint=False,
        on_delete=models.SET_NULL,
        null=True,
        related_name="to_user_id",
    )
    from_user_id = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        db_constraint=False,
        null=True,
        related_name="from_user_id",
    )
    is_anonymous = models.BooleanField(default=False)
    writing_pad_id = models.ForeignKey(
        WritingPad,
        db_constraint=False,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name="writing_pad_id",
    )
    envelope_id = models.ForeignKey(
        Envelope,
        db_constraint=False,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name="envelope_id",
    )
    stamp_id = models.ForeignKey(
        Stamp,
        db_constraint=False,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name="stamp_id",
    )
    content = models.TextField()
    title = models.CharField(max_length=255)
    font = models.CharField(max_length=50)
    will_arrive_at = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Letter"
        indexes = [
            models.Index(fields=["to_user_id"]),
            models.Index(fields=["from_user_id"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.title


class LetterRelation(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    target_letter_id = models.ForeignKey(
        Letter,
        db_constraint=False,
        on_delete=models.CASCADE,
        null=True,
        default=None,
        related_name="target_letter_id",
    )
    reply_letter_id = models.ForeignKey(
        Letter,
        db_constraint=False,
        on_delete=models.CASCADE,
        null=True,
        default=None,
        related_name="reply_letter_id",
    )

    class Meta:
        db_table = "LetterRelation"
