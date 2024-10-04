import uuid
from datetime import datetime

from lucky_letter.domain.letter import FontType
from lucky_letter.domain.letter import Letter as LetterVo
from lucky_letter.domain.letter import LetterGroup as LetterGroupVo
from lucky_letter.infra.repo.letter_repo import LetterGroupRepo, LetterRepo
from lucky_letter.service.i_repo.i_letter_repo import ILetterGroupRepo, ILetterRepo


class LetterService:
    def __init__(self) -> None:
        # TODO: DI 적용
        self.letter_repo: ILetterRepo = LetterRepo()
        self.letter_group_repo: ILetterGroupRepo = LetterGroupRepo()

    def create_letter(
        self,
        to_app_id: str | None,
        letter_group_id: str | None,
        from_app_id: str,
        is_anonymous: bool,
        writing_pad_id: str,
        envelope_id: str,
        stamp_id: str,
        content: str,
        title: str,
        font: FontType,
        will_arrive_at: str | None = None,
    ) -> LetterVo:
        # 만약 letter 가 그룹이 없다면 새로 생성
        if letter_group_id is None:
            letter_group_vo = LetterGroupVo(
                id=str(uuid.uuid4()),
                name=str(uuid.uuid4()),  # 일단은 이렇게 해둡시다.
                created_at=datetime.now().isoformat(),
            )
            letter_group_id = letter_group_vo.id
            self.letter_group_repo.create(letter_group_vo=letter_group_vo)

        letter = LetterVo(
            id=str(uuid.uuid4()),
            letter_group_id=letter_group_id,
            to_app_id=to_app_id,
            from_app_id=from_app_id,
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
        return self.letter_repo.create(letter_vo=letter)

        # 그냥 저장.
        # 후 LETTER 객체 반환.
