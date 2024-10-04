from dataclasses import dataclass
from enum import StrEnum

from common.domain import Domain


@dataclass
class LetterGroup(Domain):
    FIELD_ID = "id"
    FIELD_NAME = "name"
    FIELD_CREATED_AT = "created_at"

    id: str
    name: str
    created_at: str


class FontType(StrEnum):
    NATO_SANS_KR = "NATO_SANS_KR"
    # 어떤것들이 있을거임


@dataclass
class Letter(Domain):
    """
    편지 도메인 모델
    """

    FIELD_ID = "id"
    FIELD_TO_APP_ID = "to_app_id"
    FIELD_FROM_APP_ID = "from_app_id"
    FIELD_LETTER_GROUP_ID = "letter_group_id"
    FIELD_IS_ANONYMOUS = "is_anonymous"
    FIELD_WRITING_PAD_ID = "writing_pad_id"
    FIELD_ENVELOPE_ID = "envelope_id"
    FIELD_STAMP_ID = "stamp_id"
    FIELD_CONTENT = "content"
    FIELD_TITLE = "title"
    FIELD_FONT = "font"
    FIELD_WILL_ARRIVE_AT = "will_arrive_at"

    id: str
    to_app_id: str | None  # 특정 상대에게 보내는게 아닌 경우 None
    letter_group_id: str
    from_app_id: str
    is_anonymous: bool
    writing_pad_id: str  # 편지지
    envelope_id: str  # 편지봉투
    stamp_id: str  # 우표
    content: str
    title: str
    font: FontType
    will_arrive_at: str  # 도착 시간을 명시할 경우


@dataclass
class WritingPad(Domain):
    """
    편지지 도메인 모델
    """

    FIELD_ID = "id"
    FIELD_NAME = "name"
    FIELD_URL = "url"

    id: str
    name: str
    url: str


@dataclass
class Envelope(Domain):
    """
    편지봉투 도메인 모델
    """

    FIELD_ID = "id"
    FIELD_NAME = "name"
    FIELD_URL = "url"

    id: str
    name: str
    url: str


@dataclass
class Stamp(Domain):
    """
    우표 도메인 모델
    """

    FIELD_ID = "id"
    FIELD_NAME = "name"
    FIELD_URL = "url"

    id: str
    name: str
    url: str
