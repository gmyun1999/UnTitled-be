from typing import Any

from django.db import DatabaseError

from notification.domain.notification import NotificationType
from user.domain.user import User as UserVo
from user.domain.user_notification import UserNotification as UserNotificationVo
from user.domain.user_notification import (
    UserNotificationSetting as UserNotificationSettingVo,
)
from user.infra.models.nested_serializer import NestedUserNotificationSerializer
from user.infra.models.notification_model import (
    UserNotification,
    UserNotificationSetting,
)
from user.infra.models.serializer import (
    UserNotificationSerializer,
    UserNotificationSettingSerializer,
)
from user.service.repository.i_user_notification_repo import (
    IUserNotificationRepo,
    IUserNotificationSettingRepo,
)


class UserNotificationRepo(IUserNotificationRepo):
    def get_user_notification(
        self, filter: IUserNotificationRepo.Filter
    ) -> list[dict[str, Any] | None]:
        user_notification = UserNotification.objects.all()
        if filter.notification_id:
            user_notification = user_notification.filter(
                notification=filter.notification_id
            )
        if filter.user_id:
            user_notification = user_notification.filter(user_id=filter.user_id)

        serializer = NestedUserNotificationSerializer(user_notification, many=True)
        return serializer.data

    def save_user_notification(
        self, user_notification_vo: UserNotificationVo
    ) -> UserNotificationVo:
        dicted = user_notification_vo.to_dict()
        serializer = UserNotificationSerializer(data=dicted)
        if serializer.is_valid():
            serializer.save()
            return user_notification_vo

        else:
            raise DatabaseError(serializer.errors)

    def mark_as_read(self, user_notification_id: str) -> dict[str, Any]:
        user_notification = UserNotification.objects.get(id=user_notification_id)
        user_notification.mark_as_read()
        serializer = UserNotificationSerializer(user_notification)
        return serializer.data


class UserNotificationSettingRepo(IUserNotificationSettingRepo):
    def get_user_settings(
        self, filter: IUserNotificationSettingRepo.Filter
    ) -> list[dict[str, Any] | None]:
        user_notification_setting = UserNotificationSetting.objects.all()

        if filter.user_id:
            user_notification_setting = user_notification_setting.filter(
                user_id=filter.user_id
            )
        if filter.notification_type:
            user_notification_setting = user_notification_setting.filter(
                notification_type=filter.notification_type.value
            )

        serializer = UserNotificationSettingSerializer(
            user_notification_setting, many=True
        )
        return serializer.data

    def save_user_settings(
        self, user_notification_setting: UserNotificationSettingVo
    ) -> UserNotificationSettingVo:
        dicted = user_notification_setting.to_dict()
        serializer = UserNotificationSettingSerializer(data=dicted)
        if serializer.is_valid():
            serializer.save()
            return user_notification_setting
        else:
            raise DatabaseError(serializer.errors)

    def modify_user_settings(
        self, user: UserVo, notification_type: NotificationType, is_push_allow: bool
    ) -> UserNotificationSettingVo:
        previous_instance = UserNotificationSetting.objects.get(
            user_id=user.id, notification_type=notification_type.value
        )
        data = {UserNotificationSettingVo.FIELD_IS_PUSH_ALLOW: is_push_allow}

        serializer = UserNotificationSettingSerializer(
            previous_instance,
            data=data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return UserNotificationSettingVo.from_dict(data)
        else:
            raise DatabaseError(serializer.errors)
