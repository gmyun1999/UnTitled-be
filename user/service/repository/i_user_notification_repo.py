from abc import ABCMeta, abstractmethod
from typing import Any

from common.domain import Domain
from notification.domain.notification import NotificationType
from user.domain.user import User as UserVo
from user.domain.user_notification import UserNotification as UserNotificationVo
from user.domain.user_notification import (
    UserNotificationSetting as UserNotificationSettingVo,
)


class IUserNotificationRepo(metaclass=ABCMeta):
    class Filter:
        def __init__(
            self, user_id: str | None = None, notification_id: str | None = None
        ):
            self.user_id = user_id
            self.notification_id = notification_id

    @abstractmethod
    def get_user_notification(self, filter: Filter) -> list[dict[str, Any] | None]:
        pass

    @abstractmethod
    def save_user_notification(
        self, user_notification_vo: UserNotificationVo
    ) -> UserNotificationVo:
        pass

    @abstractmethod
    def mark_as_read(self, user_notification_id: str) -> dict[str, Any] | None:
        pass


class IUserNotificationSettingRepo(metaclass=ABCMeta):
    class Filter:
        def __init__(
            self,
            user_id: str | None = None,
            is_push_allow: bool | None = None,
            notification_type: NotificationType | None = None,
        ):
            self.user_id = user_id
            self.notification_type = notification_type
            self.is_push_allow = is_push_allow

    @abstractmethod
    def get_user_settings(self, filter: Filter) -> list[dict[str, Any] | None]:
        pass

    @abstractmethod
    def save_user_settings(
        self, user_notification_setting: UserNotificationSettingVo
    ) -> UserNotificationSettingVo:
        pass

    @abstractmethod
    def modify_user_settings(
        self, user: UserVo, notification_type: NotificationType, is_push_allow: bool
    ) -> UserNotificationSettingVo:
        pass
