from dataclasses import dataclass
from typing import Literal

from django.http import HttpRequest
from pydantic import BaseModel, Field
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from common.interface.http_response import standard_response
from common.interface.validators import validate_body
from user.domain.user_role import UserRole
from user.domain.user_token import PushServiceType, UserTokenPayload, UserTokenType
from user.infra.token.user_token_manager import UserTokenManager
from user.interface.validator.user_token_validator import validate_token
from user.service.user_push_service import UserPushService
from user.service.user_service import UserService


class RefreshTokenView(APIView):
    def __init__(self):
        self.user_service = UserService()

    @validate_token(
        roles=[UserRole.USER, UserRole.ADMIN], validate_type=UserTokenType.ACCESS
    )
    def get(
        self,
        request: HttpRequest,
        token_payload: UserTokenPayload,
    ):
        if token_payload.admin_id is not None:
            user_id = token_payload.admin_id
        elif token_payload.user_id is not None:
            user_id = token_payload.user_id

        token: dict = self.user_service.create_user_token(user_id=user_id)

        return standard_response(
            message="refresh user token", data=token, http_status=status.HTTP_200_OK
        )


@dataclass
class PushTokenBody(BaseModel):
    push_server: Literal[PushServiceType.FCM]
    token: str = Field(max_length=4020)


@api_view(["POST"])
@validate_token(
    roles=[UserRole.USER], validate_type=UserTokenType.ACCESS, view_type="function"
)
@validate_body(PushTokenBody, view_type="function")
def save_push_service_token(
    request, token_payload: UserTokenPayload, body: PushTokenBody
):
    user_token_manager = UserTokenManager()
    user_push_service = UserPushService()
    current_user = user_token_manager.get_current_user(user_payload_vo=token_payload)
    user_push_token = user_push_service.save_push_service_token(
        token=body.token, user=current_user, service_type=body.push_server
    )
    if user_push_token is None:
        return standard_response(
            message="invalid push token",
            data="",
            http_status=status.HTTP_400_BAD_REQUEST,
        )

    return standard_response(
        message="save token successfully",
        data=user_push_token.to_dict(),
        http_status=status.HTTP_201_CREATED,
    )
