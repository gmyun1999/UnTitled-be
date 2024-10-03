from dataclasses import dataclass, field
from datetime import datetime

from notification.domain.notification import NotificationDomain


@dataclass
class UserNotificationDomain:
    user_id: int
    notification: NotificationDomain
    is_read: bool = False
    delivered_at: datetime = field(default_factory=datetime.now)

    def mark_as_read(self):
        self.is_read = True
