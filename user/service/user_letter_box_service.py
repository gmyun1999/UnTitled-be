import uuid
from typing import Any

from lucky_letter.domain.letter import Letter as LetterVo
from user.domain.user_letter_box import UserLetterBox, UserLetterBoxType
from user.infra.repository.user_letter_box import UserLetterBoxRepo
from user.service.repository.i_user_letter_box import IUserLetterBoxRepo


class UserLetterBoxService:
    def __init__(self):
        # TODO: Di 적용
        self.letter_box_repo: IUserLetterBoxRepo = UserLetterBoxRepo()

    def fetch_letter(self, letter_id: str, user_id: str) -> dict[str, Any] | None:
        return self.letter_box_repo.get_my_letter(letter_id=letter_id, user_id=user_id)

    def fetch_sended_letter(self, user_id: str) -> list[dict[str, Any]] | None:
        return self.letter_box_repo.fetch_my_letters(
            user_id=user_id, letter_type=UserLetterBoxType.SENT
        )

    def fetch_received_letter(self, user_id: str) -> list[dict[str, Any]] | None:
        return self.letter_box_repo.fetch_my_letters(
            user_id=user_id, letter_type=UserLetterBoxType.RECEIVED
        )

    def store_letter(self, letter_vo: LetterVo, user_id: str, type: UserLetterBoxType):
        user_letter_box_vo = UserLetterBox(
            id=str(uuid.uuid4()),
            user_id=user_id,
            letter_id=letter_vo.id,
            type=type,
            is_read=False,
        )
        self.letter_box_repo.store_letter_in_letter_box(user_letter_box_vo)

    def delete_sended_letter(self, letter_id: str, user_id: str):
        pass

    def delete_received_letter(self, letter_id: str, user_id: str):
        pass
