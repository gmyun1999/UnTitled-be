from dataclasses import dataclass
from typing import Any, Literal

from pydantic import BaseModel, Field
from rest_framework import status
from rest_framework.views import APIView

from common.interface.http_response import standard_response
from common.interface.validators import validate_query_params
from notification.domain.notification import NotificationType
from user.domain.user_role import UserRole
from user.domain.user_token import UserTokenPayload, UserTokenType
from user.infra.token.user_token_manager import UserTokenManager
from user.interface.validator.user_token_validator import validate_token
from user.service.user_service import UserNotificationService


class UserNotificationView(APIView):
    def __init__(self):
        self.user_notification_service = UserNotificationService()
        self.user_token_manager = UserTokenManager()

    @validate_token(roles=[UserRole.USER], validate_type=UserTokenType.ACCESS)
    def get(self, request, token_payload: UserTokenPayload):
        """
        알림 가져오기
        """
        current_user = self.user_token_manager.get_current_user(
            user_payload_vo=token_payload
        )
        my_notification = self.user_notification_service.get_my_notification(
            user_vo=current_user
        )
        return standard_response(
            message="fetch my notification",
            data=my_notification,
            http_status=status.HTTP_200_OK,
        )


class UserNotificationSettingView(APIView):
    @dataclass
    class GetNotificationSettingParams(BaseModel):
        notification_type: NotificationType | None = Field(default=None)

    @dataclass
    class PutNotificationSettingParams(BaseModel):
        is_push_allow: bool
        notification_type: NotificationType | None = Field(default=None)

    def __init__(self):
        self.user_notification_service = UserNotificationService()
        self.user_token_manager = UserTokenManager()

    @validate_token(roles=[UserRole.USER], validate_type=UserTokenType.ACCESS)
    @validate_query_params(GetNotificationSettingParams)
    def get(
        self,
        request,
        token_payload: UserTokenPayload,
        params: GetNotificationSettingParams,
    ):
        """
        알림 세팅 불러오기
        """
        current_user = self.user_token_manager.get_current_user(
            user_payload_vo=token_payload
        )

        if params.notification_type is not None:
            my_notification_setting = (
                self.user_notification_service.get_my_specific_notification_setting(
                    user_vo=current_user, notification_type=params.notification_type
                )
            )
        else:
            my_notification_setting = (
                self.user_notification_service.get_my_notification_setting(
                    user_vo=current_user
                )
            )

        return standard_response(
            message="fetch my notification setting",
            data=my_notification_setting,
            http_status=status.HTTP_200_OK,
        )

    @validate_token(roles=[UserRole.USER], validate_type=UserTokenType.ACCESS)
    @validate_query_params(PutNotificationSettingParams)
    def put(
        self,
        request,
        token_payload: UserTokenPayload,
        params: PutNotificationSettingParams,
    ):
        """
        알림 세팅 변경하기
        """
        current_user = self.user_token_manager.get_current_user(
            user_payload_vo=token_payload
        )

        updated_my_notification_setting = (
            self.user_notification_service.update_my_notification_setting(
                user_vo=current_user,
                is_push_allow=params.is_push_allow,
                notification_type=params.notification_type,
            )
        )

        data = [item.to_dict() for item in updated_my_notification_setting]

        return standard_response(
            message="update my notification setting",
            data=data,
            http_status=status.HTTP_200_OK,
        )
