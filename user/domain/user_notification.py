from dataclasses import dataclass, field
from datetime import datetime

from common.domain import Domain
from notification.domain.notification import NotificationType


@dataclass
class UserNotification(Domain):
    user_id: int
    notification_id: str
    is_read: bool = False

    delivered_at: datetime = field(default_factory=datetime.now)

    def mark_as_read(self):
        self.is_read = True


@dataclass
class UserNotificationSetting(Domain):
    user_id: int
    notification_type: NotificationType
    is_push_allow: bool
