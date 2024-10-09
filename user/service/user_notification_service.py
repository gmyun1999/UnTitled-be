import uuid
from datetime import datetime
from typing import Any

from notification.domain.notification import Notification as NotificationVo
from notification.domain.notification import NotificationType
from user.domain.user import User as UserVo
from user.domain.user_notification import (
    PushMessage,
    UserNotification,
    UserNotificationSetting,
)
from user.infra.repository.user_notification_repo import (
    UserNotificationRepo,
    UserNotificationSettingRepo,
)
from user.service.repository.i_user_notification_repo import (
    IUserNotificationRepo,
    IUserNotificationSettingRepo,
)
from user.service.user_push_service import UserPushService


class UserNotificationService:
    def __init__(self) -> None:
        # TODO: DI 적용
        self.user_notification_repo: IUserNotificationRepo = UserNotificationRepo()
        self.user_notification_setting_repo: IUserNotificationSettingRepo = (
            UserNotificationSettingRepo()
        )
        self.user_push_service = UserPushService()

    def get_my_notification_setting(self, user_vo: UserVo):
        """
        내가 세팅해놓은 알림 상태 가져오기
        """
        filter = self.user_notification_setting_repo.Filter(user_id=user_vo.id)
        return self.user_notification_setting_repo.get_user_settings(filter=filter)

    def get_my_specific_notification_setting(
        self, user_vo: UserVo, notification_type: NotificationType
    ):
        filter = self.user_notification_setting_repo.Filter(
            user_id=user_vo.id, notification_type=notification_type
        )
        return self.user_notification_setting_repo.get_user_settings(filter=filter)

    def init_notification_setting(self, user_vo: UserVo):
        for notification_type in NotificationType:
            user_notification_setting = UserNotificationSetting(
                id=str(uuid.uuid4()),
                user_id=user_vo.id,
                notification_type=notification_type,
                is_push_allow=True,
            )
            self.user_notification_setting_repo.save_user_settings(
                user_notification_setting=user_notification_setting
            )

    def update_my_notification_setting(
        self,
        user_vo: UserVo,
        is_push_allow: bool,
        notification_type: NotificationType | None = None,
    ) -> list[UserNotificationSetting]:
        """
        내 알림 세팅 수정하기
        """
        notification_setting_result = []

        if notification_type is None:
            for notification_type_item in NotificationType:
                result = self.user_notification_setting_repo.modify_user_settings(
                    user=user_vo,
                    notification_type=notification_type_item,
                    is_push_allow=is_push_allow,
                )
                notification_setting_result.append(result)
        else:
            result = self.user_notification_setting_repo.modify_user_settings(
                user=user_vo,
                notification_type=notification_type,
                is_push_allow=is_push_allow,
            )
            notification_setting_result.append(result)
        return notification_setting_result

    def get_my_notification(self, user_vo: UserVo) -> list[dict[str, Any] | None]:
        """
        내 알림함에 있는 알림들 가져오기
        """
        filter = self.user_notification_repo.Filter(user_id=user_vo.id)
        return self.user_notification_repo.get_user_notification(filter=filter)

    def delete_my_notification(self, my_notification_id: str, is_bulk: bool = False):
        """
        내 알림함에 있는 알림들 지우기
        """
        pass

    def update_my_notification_as_read(
        self, user_notification_id: str
    ) -> dict[str, Any] | None:
        return self.user_notification_repo.mark_as_read(
            user_notification_id=user_notification_id
        )

    def save_user_notification(self, notification_vo: NotificationVo, user_vo: UserVo):
        """
        user와 notification을 이용해서 알림 객체를 저정한다.
        """
        user_notification = UserNotification(
            id=str(uuid.uuid4()),
            user_id=user_vo.id,
            notification_id=notification_vo.id,
            is_read=False,
            delivered_at=datetime.now(),
        )
        return self.user_notification_repo.save_user_notification(
            user_notification_vo=user_notification
        )

    def create_user_notification(
        self, notification_vo: NotificationVo, user_vo: UserVo
    ) -> tuple[PushMessage | None, str]:
        """
        save 시킨다음에 user_notification setting 을 확인한후에 send_push_msg를 호출한다.
        하나의 user notification을 생성한다. bulk x
        """
        self.save_user_notification(notification_vo=notification_vo, user_vo=user_vo)
        my_setting = self.get_my_specific_notification_setting(
            user_vo=user_vo, notification_type=notification_vo.notification_type
        )[0]

        if my_setting[UserNotificationSetting.FIELD_IS_PUSH_ALLOW] is True:
            msg = self.user_push_service.create_push_message(
                user=user_vo, notification=notification_vo
            )
            token = self.user_push_service.get_push_token(user=user_vo)
            if token is None:
                return None, "push token does not exist"

            push_msg, result = self.user_push_service.send_push_msg(
                msg=msg, token=token
            )
            return push_msg, result
        return None, "save user notification"

    def bulk_create_user_notification(self):
        pass
