from typing import Any, Tuple

from django.db import DatabaseError

from user.domain.user_letter_box import UserLetterBox as UserLetterBoxVo
from user.infra.models.nested_serializer import NestedUserLetterBoxSerializer
from user.infra.models.serializer import UserLetterBoxSerializer
from user.infra.models.user_letter_box_model import UserLetterBox
from user.service.repository.i_user_letter_box import IUserLetterBoxRepo


class UserLetterBoxRepo(IUserLetterBoxRepo):
    def fetch_my_letters(
        self, user_id: str, letter_type: str
    ) -> list[dict[str, Any]] | None:
        letters = UserLetterBox.objects.filter(user_id=user_id, type=letter_type)
        serializer = NestedUserLetterBoxSerializer(letters, many=True)
        return serializer.data if serializer.data else None

    def get_my_letter(self, letter_id: str, user_id: str) -> dict[str, Any] | None:
        try:
            letter = UserLetterBox.objects.get(letter_id=letter_id, user_id=user_id)

            serializer = NestedUserLetterBoxSerializer(letter)
            dicted_data = serializer.data
            return dicted_data

        except UserLetterBox.DoesNotExist:
            return None

    def letter_mark_as_read(self, letter_id: str) -> bool:
        try:
            letter = UserLetterBox.objects.get(letter_id=letter_id)
            letter.mark_as_read()
            return True

        except UserLetterBox.DoesNotExist:
            return False

    def store_letter_in_letter_box(
        self,
        UserLetterBox_vo: UserLetterBoxVo,
    ) -> None:
        data = UserLetterBox_vo.to_dict()
        serializer = UserLetterBoxSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise DatabaseError(serializer.errors)
