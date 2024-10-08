from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from common.domain import Domain


class NotificationType(StrEnum):
    SYSTEM = "SYSTEM"
    ADVERTISEMENT = "ADVERTISEMENT"
    FRIEND_REQUEST = "FRIEND_REQUEST"
    RECEIVED_LETTER = "RECEIVED_LETTER"


@dataclass
class Notification(Domain):
    FIELD_TITLE = "title"
    FIELD_MESSAGE = "message"

    id: str
    title: str
    message: str
    notification_type: NotificationType
    created_at: datetime = field(default_factory=datetime.now)
    related_object: object = None
