import uuid
from dataclasses import dataclass

from django.http import JsonResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from pydantic import BaseModel, Field
from rest_framework import status
from rest_framework.views import APIView

from common.interface.http_response import standard_response
from common.interface.validators import validate_body
from user.domain.user import User as UserVo
from user.domain.user_role import UserRole
from user.domain.user_token import UserTokenPayload, UserTokenType
from user.infra.models.swagger.user import (
    CreateUserBodyRequestSerializer,
    UserCreateStandardResponseSerializer,
    UserDuplicateCheckStandardResponseSerializer,
    ValidateBodyRequestSerializer,
)
from user.infra.token.user_token_manager import UserTokenManager
from user.interface.validator.user_token_validator import validate_token
from user.service.user_service import UserService


class UserCheckDuplicateView(APIView):
    def __init__(self):
        self.user_service = UserService()

    @dataclass
    class ValidateBody(BaseModel):
        app_id: str | None = Field(max_length=16, default=None)
        name: str | None = Field(max_length=64, default=None)

    @extend_schema(
        summary="user 중복체크 app_id, name 중복체크",
        description="중복시 is_duplicate: True, 중복이 아닐시 is_duplicate: False, tartget: app_id, name",
        request=ValidateBodyRequestSerializer,
        responses={200: UserDuplicateCheckStandardResponseSerializer},
    )
    @validate_body(ValidateBody)
    def post(self, request, body):
        if body.app_id:
            is_duplicate = self.user_service.check_duplicate_app_id(app_id=body.app_id)
            if is_duplicate:
                return standard_response(
                    message="The app_id provided is already in use.",
                    data=[{"target": "app_id", "is_duplicate": True}],
                    http_status=status.HTTP_200_OK,
                )
            else:
                return standard_response(
                    message="The app_id is available.",
                    data=[{"target": "app_id", "is_duplicate": False}],
                    http_status=status.HTTP_200_OK,
                )


class UserView(APIView):
    def __init__(self):
        self.user_service = UserService()
        self.user_token_manager = UserTokenManager()

    @dataclass
    class CreateUserBody(BaseModel):
        app_id: str = Field(max_length=16)
        name: str = Field(max_length=64)

    @extend_schema(
        summary="user 생성",
        description="app_id, name 넘기면됨,toekn 반환",
        request=CreateUserBodyRequestSerializer,
        responses={200: UserCreateStandardResponseSerializer},
    )
    @validate_body(CreateUserBody)
    def post(self, request, body: CreateUserBody):
        """
        user 생성
        id, app_id, name 받아서 userVo 만들어서 서비스로 넘기기.
        """
        is_duplicate = self.user_service.check_duplicate_app_id(app_id=body.app_id)
        if is_duplicate:
            return JsonResponse(
                data={"message": "duplicated_app_id"}, status=status.HTTP_409_CONFLICT
            )
        user = UserVo(id=str(uuid.uuid4()), app_id=body.app_id, name=body.name)
        user = self.user_service.create_user(user=user)
        token = self.user_service.create_user_token(user.id)

        return standard_response(
            message="create user successfully",
            data=token,
            http_status=status.HTTP_201_CREATED,
        )

    @validate_token(roles=[UserRole.USER], validate_type=UserTokenType.ACCESS)
    def delete(
        self,
        request,
        token_payload: UserTokenPayload,
    ):
        """
        계정삭제
        """
        current_user = self.user_token_manager.get_current_user(
            user_payload_vo=token_payload
        )
        self.user_service.delete_user(user=current_user)
        return standard_response(
            message="delete user successfully",
            data="",
            http_status=status.HTTP_200_OK,
        )


class UserMeView(APIView):
    def __init__(self):
        pass

    def get(self):
        """
        나의  user 정보 fetch
        """
        pass

    def put(self):
        """
        나의 suer 정보 update
        """
        pass

    def delete(self):
        """
        나의 user  정보 삭제하기
        """
        pass
