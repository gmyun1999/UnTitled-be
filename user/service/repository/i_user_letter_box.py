from abc import ABCMeta, abstractmethod
from typing import Any, Tuple

from user.domain.user_letter_box import UserLetterBox


class IUserLetterBoxRepo(metaclass=ABCMeta):
    @abstractmethod
    def fetch_my_letters(
        self, user_id: str, letter_type: str
    ) -> list[dict[str, Any]] | None:
        pass

    @abstractmethod
    def get_my_letter(
        self, letter_id: str
    ) -> tuple[dict[str, Any], str] | tuple[None, None]:
        pass

    @abstractmethod
    def store_letter_in_letter_box(
        self,
        UserLetterBox_vo: UserLetterBox,
    ) -> None:
        pass
