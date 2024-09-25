# sender_id, receiver_id, type, title, body, 봤는지 등

from dataclasses import dataclass
from enum import StrEnum

from common.domain import Domain


class NotificationType(StrEnum):
    RECEIVED_LETTER = "RECEIVED_LETTER"
    REQUEST_FRIEND = "REQUEST_FRIEND"


class NotificationStatus(StrEnum):
    ON = "ON"
    OFF = "OFF"


@dataclass
class Notification(Domain):
    id: str
    sender_id: str
    receiver_id: str
    type: NotificationType
    title: str  # 알림 제목
    body: str  # 알림 내용
    is_read: bool


@dataclass
class NotificationSetting(Domain):
    id: str
    type: NotificationType
    user_id: str
    notification_status: NotificationStatus
