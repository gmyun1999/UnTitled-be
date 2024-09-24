from datetime import datetime

from lucky_letter.domain.letter import FontType
from lucky_letter.domain.letter import Letter as LetterVo


class LetterService:
    def __init__(self) -> None:
        pass

    def create_letter(
        self,
        to_app_id: str,
        from_app_id: str | None,
        is_anonymous: bool,
        writing_pad_id: str,
        envelope_id: str,
        stamp_id: str,
        content: str,
        title: str,
        font: FontType,
        will_arrive_at: datetime | None = None,
    ) -> LetterVo:
        pass
        # 그냥 저장.
        # 후 LETTER 객체 반환.
