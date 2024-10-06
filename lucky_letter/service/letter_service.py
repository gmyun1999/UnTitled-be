import uuid
from datetime import datetime

from lucky_letter.domain.letter import FontType
from lucky_letter.domain.letter import Letter as LetterVo
from lucky_letter.domain.letter import LetterRelation as LetterRelationVo
from lucky_letter.infra.repo.letter_repo import LetterRelationRepo, LetterRepo
from lucky_letter.service.i_repo.i_letter_repo import ILetterRelationRepo, ILetterRepo
from user.domain.user import User as UserVo
from user.infra.repository.user_repo import UserRepo
from user.service.repository.i_user_repo import IUserRepo


class LetterService:
    def __init__(self) -> None:
        # TODO: DI 적용
        self.letter_repo: ILetterRepo = LetterRepo()
        self.letter_relation_repo: ILetterRelationRepo = LetterRelationRepo()
        self.user_repo: IUserRepo = UserRepo()

    def get_letter_relation(self, target_letter_id: str) -> LetterRelationVo | None:
        return self.letter_relation_repo.get_letter_relation(
            target_letter_id=target_letter_id
        )

    def get_reply_letter(self, target_letter_id: str):
        letter_relation = self.get_letter_relation(target_letter_id=target_letter_id)
        if letter_relation is None:
            return None

        reply_letter_id = letter_relation.reply_letter_id
        return self.get_letter_by_id(letter_id=reply_letter_id)

    def get_letter_by_id(self, letter_id: str) -> LetterVo | None:
        filter = self.letter_repo.Filter(id=letter_id)
        return self.letter_repo.get_letter(filter=filter)

    def create_letter(
        self,
        to_letter_id: str | None,
        to_user: UserVo,
        from_user: UserVo,
        is_anonymous: bool,
        writing_pad_id: str,
        envelope_id: str,
        stamp_id: str,
        content: str,
        title: str,
        font: FontType,
        will_arrive_at: str | None = None,
    ) -> LetterVo:
        letter = LetterVo(
            id=str(uuid.uuid4()),
            to_user_id=to_user.id,
            from_user_id=from_user.id,
            is_anonymous=is_anonymous,
            writing_pad_id=writing_pad_id,
            envelope_id=envelope_id,
            stamp_id=stamp_id,
            content=content,
            title=title,
            font=font,
            will_arrive_at=will_arrive_at
            if will_arrive_at is not None
            else datetime.now().isoformat(),
        )
        letter = self.letter_repo.create(letter_vo=letter)

        if to_letter_id is not None:
            letter_relation = LetterRelationVo(
                id=str(uuid.uuid4()),
                target_letter_id=to_letter_id,
                reply_letter_id=letter.id,
            )
            self.letter_relation_repo.create(letter_relation_vo=letter_relation)

        return letter

        # 그냥 저장.
        # 후 LETTER 객체 반환.
