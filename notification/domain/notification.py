from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from user.domain.user import User


class NotificationType(StrEnum):
    SYSTEM = "SYSTEM"
    ADVERTISEMENT = "ADVERTISEMENT"
    FRIEND_REQUEST = "FRIEND_REQUEST"
    SENT_LETTER = "SENT_LETTER"
    ARRIVAL = "ARRIVAL"


@dataclass
class NotificationDomain:
    title: str
    message: str
    notification_type: NotificationType
    is_system_wide: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    related_object: object = None
