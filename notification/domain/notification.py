from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from common.domain import Domain


class NotificationType(StrEnum):
    SYSTEM = "SYSTEM"
    ADVERTISEMENT = "ADVERTISEMENT"
    FRIEND_REQUEST = "FRIEND_REQUEST"
    RECEIVED_LETTER = "RECEIVED_LETTER"


class NotificationRelatedDomain(StrEnum):
    Letter = "Letter"
    UserRelation = "UserRelation"


@dataclass
class Notification(Domain):
    FIELD_TITLE = "title"
    FIELD_MESSAGE = "message"

    id: str
    title: str
    message: str
    notification_type: NotificationType
    related_domain: NotificationRelatedDomain | None
    related_object_id: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
