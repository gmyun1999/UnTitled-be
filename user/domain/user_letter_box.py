from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from common.domain import Domain


class UserLetterBoxType(StrEnum):
    SENT = "SENT"
    RECEIVED = "RECEIVED"


@dataclass
class UserLetterBox(Domain):
    FIELD_USER_ID = "user_id"
    FIELD_LETTER_ID = "letter_id"

    id: str
    user_id: str
    letter_id: str
    type: UserLetterBoxType
    is_read: bool = False
    delivered_at: datetime = field(default_factory=datetime.now)

    def mark_as_read(self):
        self.is_read = True
