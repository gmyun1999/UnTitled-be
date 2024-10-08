from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from common.domain import Domain
from user.domain.user import User


class NotificationType(StrEnum):
    SYSTEM = "SYSTEM"
    ADVERTISEMENT = "ADVERTISEMENT"
    FRIEND_REQUEST = "FRIEND_REQUEST"
    SENT_LETTER = "SENT_LETTER"
    RECEIVED_LETTER = "RECEIVED_LETTER"


@dataclass
class Notification(Domain):
    id: str
    title: str
    message: str
    notification_type: NotificationType
    delivered_at: datetime
    is_system_wide: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    related_object: object = None
