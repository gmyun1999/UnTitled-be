from dataclasses import dataclass
from enum import StrEnum


class FontType(StrEnum):
    NATO_SANS_KR = "NATO_SANS_KR"
    # 어떤것들이 있을거임


@dataclass
class Letter:
    """
    편지 도메인 모델
    """

    FIELD_ID = "id"
    FIELD_TO_ID = "to_id"
    FIELD_FROM_ID = "from_id"
    FIELD_IS_ANONYMOUS = "is_anonymous"
    FIELD_WRITING_PAD_ID = "writing_pad_id"
    FIELD_ENVELOPE_ID = "envelope_id"
    FIELD_STAMP_ID = "stamp_id"
    FIELD_CONTENT = "content"
    FIELD_TITLE = "title"
    FIELD_FONT = "font"
    FIELD_WILL_ARRIVE_AT = "will_arrive_at"
    FIELD_CREATED_AT = "created_at"
    FIELD_UPDATED_AT = "updated_at"

    id: str
    to_id: str
    from_id: str | None  # 특정 상대에게 보내는게 아닌 경우 None
    is_anonymous: bool
    writing_pad_id: str  # 편지지
    envelope_id: str  # 편지봉투
    stamp_id: str  # 우표
    content: str
    title: str
    font: FontType
    will_arrive_at: str  # 도착 시간을 명시할 경우
    created_at: str
    updated_at: str


@dataclass
class WritingPad:
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
class Envelope:
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
class Stamp:
    """
    우표 도메인 모델
    """

    FIELD_ID = "id"
    FIELD_NAME = "name"
    FIELD_URL = "url"

    id: str
    name: str
    url: str
