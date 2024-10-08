from typing import Any

from rest_framework import status
from rest_framework.views import APIView

from common.interface.http_response import standard_response
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
    @validate_token(roles=[UserRole.USER], validate_type=UserTokenType.ACCESS)
    def get(
        self,
        request,
        token_payload: UserTokenPayload,
    ):
        """
        알림 세팅 불러오기
        """
        pass

    def put(
        self,
        request,
        token_payload: UserTokenPayload,
    ):
        """
        알림 세팅 변경하기
        """
