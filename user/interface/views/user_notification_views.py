from dataclasses import dataclass

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from pydantic import BaseModel, Field
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from common.interface.http_response import standard_response
from common.interface.validators import validate_body, validate_query_params
from common.paging import Paginator
from notification.domain.notification import NotificationType
from user.domain.user_role import UserRole
from user.domain.user_token import UserTokenPayload, UserTokenType
from user.infra.models.swagger.user_notification import (
    GetAllUserNotificationSettingSerializer,
    GetNestedPagingUserNotificationSerializer,
    GetNestedUserNotificationSerializer,
    GetUserNotificationSerializer,
    GetUserNotificationSettingSerializer,
    PutNotificationBodyRequestSerializer,
    PutUserNotificationSettingSerializer,
)
from user.infra.models.swagger.user_relation.post import ErrorResponseSerializer
from user.infra.token.user_token_manager import UserTokenManager
from user.interface.validator.user_token_validator import validate_token
from user.service.user_notification_service import UserNotificationService


@dataclass
class PutNotificationBody(BaseModel):
    is_read: bool


@extend_schema(
    summary="알림 상태 변경",
    description="읽음으로 변경",
    responses={
        200: GetUserNotificationSerializer,
        400: OpenApiResponse(
            response=ErrorResponseSerializer, description="no notification id"
        ),
    },
    request=PutNotificationBodyRequestSerializer,
)
@api_view(["PUT"])
@validate_token(
    roles=[UserRole.USER], validate_type=UserTokenType.ACCESS, view_type="function"
)
@validate_body(PutNotificationBody, view_type="function")
def update_my_notification_as_read(
    request,
    my_notification_id: str,
    token_payload: UserTokenPayload,
    body: PutNotificationBody,
):
    """
    알림 읽음으로 변경
    """
    user_token_manager = UserTokenManager()
    user_notification_service = UserNotificationService()
    current_user = user_token_manager.get_current_user(user_payload_vo=token_payload)
    # TODO: notification_id가 current user꺼인지 확인해야함
    my_notification = user_notification_service.update_my_notification_as_read(
        user_notification_id=my_notification_id
    )
    if my_notification is None:
        return standard_response(
            message="no notification id",
            data="",
            http_status=status.HTTP_400_BAD_REQUEST,
        )

    return standard_response(
        message="update as read", data=my_notification, http_status=status.HTTP_200_OK
    )


class PageParams(BaseModel):
    page: int | None = Field(default=None, ge=1)
    page_size: int | None = Field(default=None, ge=1)


class UserNotificationView(APIView):
    def __init__(self):
        self.user_notification_service = UserNotificationService()
        self.user_token_manager = UserTokenManager()

    @extend_schema(
        summary="알림 가져오기",
        description="알림을 가져옴. 쿼리파람 안념겨주면 전체 알림을 가져옴 items 안에있는 배열이 반환됨",
        responses={200: GetNestedPagingUserNotificationSerializer},
        parameters=[
            OpenApiParameter("page", OpenApiTypes.INT, description="페이지 번호"),
            OpenApiParameter("page_size", OpenApiTypes.INT, description="페이지 크기"),
        ],
    )
    @validate_token(roles=[UserRole.USER], validate_type=UserTokenType.ACCESS)
    @validate_query_params(PageParams, view_type="class")
    def get(self, request, token_payload: UserTokenPayload, params: PageParams):
        """
        알림 가져오기
        """
        current_user = self.user_token_manager.get_current_user(
            user_payload_vo=token_payload
        )
        my_notification = self.user_notification_service.get_my_notification(
            user_vo=current_user
        )
        if params.page is None or params.page_size is None:
            return standard_response(
                message="fetch my notification",
                data=my_notification,
                http_status=status.HTTP_200_OK,
            )

        paged_result = Paginator.paginate(
            items=my_notification,
            page=params.page,
            page_size=params.page_size,
        )
        response_data = {
            "items": paged_result.items,
            "total_items": paged_result.total_items,
            "total_pages": paged_result.total_pages,
            "current_page": paged_result.current_page,
            "page_size": paged_result.page_size,
            "has_previous": paged_result.has_previous,
            "has_next": paged_result.has_next,
        }
        return standard_response(
            message="fetch my notification",
            data=response_data,
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

    @extend_schema(
        summary="알림 세팅 가져오기",
        description="알림 세팅 가져오기 쿼리 파람 안주면 전체 알림 세팅을 가져옴, items 안에있는 배열이 반환됨",
        responses={200: GetAllUserNotificationSettingSerializer},
        parameters=[
            OpenApiParameter(
                "notification_type",
                OpenApiTypes.STR,
                description="알림 타입 (SYSTEM, ADVERTISEMENT, FRIEND_REQUEST, RECEIVED_LETTER)",
                required=False,
            )
        ],
    )
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

    @extend_schema(
        summary="알림 세팅 업데이트 ",
        description="알림 세팅 업데이트 notification_type를 안주면 전체 알림 세팅을 업데이트함",
        responses={200: PutUserNotificationSettingSerializer},
        parameters=[
            OpenApiParameter(
                "notification_type",
                OpenApiTypes.STR,
                description="알림 타입 (SYSTEM, ADVERTISEMENT, FRIEND_REQUEST, RECEIVED_LETTER)",
                required=False,
            ),
            OpenApiParameter(
                "is_push_allow", OpenApiTypes.BOOL, description="push 허용여부"
            ),
        ],
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
