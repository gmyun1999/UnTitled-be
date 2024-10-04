from django.db import models


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


class LetterGroup(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    name = models.CharField(max_length=36)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "LetterGroup"
        indexes = [
            models.Index(fields=["created_at"]),
        ]


class Letter(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    letter_group_id = models.CharField(max_length=36, null=True)
    to_app_id = models.CharField(max_length=36, null=True, default=None)
    from_app_id = models.CharField(max_length=36)
    is_anonymous = models.BooleanField(default=False)
    writing_pad_id = models.CharField(max_length=36)
    envelope_id = models.CharField(max_length=36)
    stamp_id = models.CharField(max_length=36)
    content = models.TextField()
    title = models.CharField(max_length=255)
    font = models.CharField(max_length=50)
    will_arrive_at = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Letter"
        indexes = [
            models.Index(fields=["to_app_id"]),
            models.Index(fields=["from_app_id"]),
            models.Index(fields=["letter_group_id"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.title
