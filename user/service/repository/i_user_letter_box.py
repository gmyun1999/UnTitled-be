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
    def get_my_letter(self, letter_id: str, user_id: str) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def letter_mark_as_read(self, letter_id: str) -> bool:
        pass

    @abstractmethod
    def store_letter_in_letter_box(
        self,
        UserLetterBox_vo: UserLetterBox,
    ) -> None:
        pass
