from typing import Any, Tuple

from django.db import DatabaseError

from user.domain.user_letter_box import UserLetterBox as UserLetterBoxVo
from user.infra.models.serializer import (
    NestedUserLetterBoxSerializer,
    UserLetterBoxSerializer,
)
from user.infra.models.user import UserLetterBox
from user.service.repository.i_user_letter_box import IUserLetterBoxRepo


class UserLetterBoxRepo(IUserLetterBoxRepo):
    def fetch_my_letters(
        self, user_id: str, letter_type: str
    ) -> list[dict[str, Any]] | None:
        letters = UserLetterBox.objects.filter(user_id=user_id, type=letter_type)
        serializer = NestedUserLetterBoxSerializer(letters, many=True)
        return serializer.data if serializer.data else None

    def get_my_letter(
        self, letter_id: str
    ) -> tuple[dict[str, Any], str] | tuple[None, None]:
        try:
            letter = UserLetterBox.objects.get(id=letter_id)

            serializer = NestedUserLetterBoxSerializer(letter)
            dicted_data = serializer.data
            return dicted_data, dicted_data[UserLetterBoxVo.FIELD_USER_ID]
        except UserLetterBox.DoesNotExist:
            return None, None

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
