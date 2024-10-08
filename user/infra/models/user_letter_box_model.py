from django.db import models

from lucky_letter.infra.models.letter_model import Letter
from user.infra.models.user_model import User


class UserLetterBox(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.ForeignKey(
        to=User,
        max_length=36,
        db_constraint=False,
        on_delete=models.CASCADE,
        related_name="user_letter_box_user_id",
        null=True,
    )
    letter_id = models.ForeignKey(
        to=Letter,
        max_length=36,
        db_constraint=False,
        on_delete=models.CASCADE,
        related_name="user_letter_box_letter_id",
        null=True,
    )
    type = models.CharField(max_length=10)
    is_read = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()
