import uuid
from dataclasses import dataclass
from typing import Any, Literal

from django.http import HttpRequest, JsonResponse
from pydantic import BaseModel, Field
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from common.interface.http_response import standard_response
from common.interface.validators import validate_body, validate_query_params
from common.service.token.i_token_manager import ITokenManager
from user.domain.user import RelationStatus, RelationType
from user.domain.user import User as UserVo
from user.domain.user_role import UserRole
from user.domain.user_token import UserTokenPayload, UserTokenType
from user.infra.token.user_token_manager import UserTokenManager
from user.interface.validator.user_token_validator import validate_token
from user.service.user_service import (
    UserLetterBoxService,
    UserRelationService,
    UserService,
)


class UserCheckDuplicateView(APIView):
    def __init__(self):
        self.user_service = UserService()

    @dataclass
    class ValidateBody(BaseModel):
        app_id: str | None = Field(max_length=16, default=None)
        name: str | None = Field(max_length=64, default=None)

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

    @dataclass
    class CreateUserBody(BaseModel):
        app_id: str = Field(max_length=16)
        name: str = Field(max_length=64)

    def get(self):
        """
        조건에 맞는 user 혹은 users fetch
        """
        pass

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


class MyRelationshipsView(APIView):
    def __init__(self):
        self.user_relation_service = UserRelationService()
        self.user_service = UserService()
        self.user_token_manager: ITokenManager = UserTokenManager()

    @dataclass
    class GetRelationParams(BaseModel):
        relation: Literal[RelationType.FRIEND] | None = None
        status: Literal[
            RelationStatus.PENDING, RelationStatus.REJECT, RelationStatus.ACCEPT
        ] | None = None

    @dataclass
    class CreateRelationParams(BaseModel):
        relation: Literal[RelationType.FRIEND]
        status: Literal[RelationStatus.PENDING]
        to_app_id: str = Field(max_length=16)

    @dataclass
    class UpdateRelationParams(BaseModel):
        relation: Literal[RelationType.FRIEND]
        status: Literal[RelationStatus.REJECT, RelationStatus.ACCEPT]
        to_app_id: str = Field(max_length=16)

    @dataclass
    class DeleteRelationParams(BaseModel):
        relation: Literal[RelationType.FRIEND]
        to_app_id: str = Field(max_length=16)

    @validate_token(roles=[UserRole.USER], validate_type=UserTokenType.ACCESS)
    @validate_query_params(GetRelationParams)
    def get(
        self,
        request: HttpRequest,
        token_payload: UserTokenPayload,
        params: GetRelationParams,
    ):
        user = self.user_token_manager.get_current_user(user_payload_vo=token_payload)
        user_relation = self.user_relation_service.get_relations(
            user_id=user.id,
            relation_status=params.status,
            relation_type=params.relation,
        )
        data: dict = {"relation": user_relation}
        return standard_response(
            message="fetch user relation", data=data, http_status=status.HTTP_200_OK
        )

    @validate_token(roles=[UserRole.USER], validate_type=UserTokenType.ACCESS)
    @validate_body(CreateRelationParams)
    def post(
        self,
        request: HttpRequest,
        token_payload: UserTokenPayload,
        body: CreateRelationParams,
    ):
        current_user = self.user_token_manager.get_current_user(
            user_payload_vo=token_payload
        )
        to_user = self.user_service.get_user_by_app_id(app_id=body.to_app_id)

        if to_user is None:
            return standard_response(
                message="to_id is not exist", http_status=status.HTTP_404_NOT_FOUND
            )

        user_relation = self.user_relation_service.create_relation(
            to_id=to_user.id,
            from_id=current_user.id,
            relation_type=body.relation,
            relation_status=body.status,
        )

        if user_relation is None:
            return standard_response(
                message="already request relation or have relation",
                http_status=status.HTTP_409_CONFLICT,
            )
        return standard_response(
            message="relation created",
            data=user_relation.to_dict(),
            http_status=status.HTTP_201_CREATED,
        )

    @validate_token(roles=[UserRole.USER], validate_type=UserTokenType.ACCESS)
    @validate_body(UpdateRelationParams)
    def put(
        self,
        request: HttpRequest,
        token_payload: UserTokenPayload,
        body: UpdateRelationParams,
    ):
        """
        이미 관계가 있는사람과의 관계를 update 하는거임.
        내가 요청한관계를 업데이트하는게아니라, 내가 받은 관계를 업데이트하는거임
        eX) 친구 요청이 있는데 이를 수락한다. 혹은 거절한다.
        """
        current_user = self.user_token_manager.get_current_user(
            user_payload_vo=token_payload
        )
        to_user = self.user_service.get_user_by_app_id(app_id=body.to_app_id)
        if to_user is None:
            return standard_response(
                message="to_id is not exist", http_status=status.HTTP_404_NOT_FOUND
            )

        user_relation = self.user_relation_service.update_my_relation(
            my_id=current_user.id,
            requested_id=to_user.id,
            relation_status=body.status,
            relation_type=body.relation,
        )

        if user_relation is None:
            return standard_response(
                message="relation not found", http_status=status.HTTP_404_NOT_FOUND
            )

        return standard_response(
            message="update relation", http_status=status.HTTP_200_OK
        )

    @validate_token(roles=[UserRole.USER], validate_type=UserTokenType.ACCESS)
    @validate_body(DeleteRelationParams)
    def delete(
        self,
        request: HttpRequest,
        token_payload: UserTokenPayload,
        body: UpdateRelationParams,
    ):
        current_user = self.user_token_manager.get_current_user(
            user_payload_vo=token_payload
        )
        to_user = self.user_service.get_user_by_app_id(app_id=body.to_app_id)
        if to_user is None:
            return standard_response(
                message="to_id is not exist", http_status=status.HTTP_404_NOT_FOUND
            )

        _ = self.user_relation_service.delete_my_relation(
            my_id=current_user.id,
            to_id=to_user.id,
            relation_status=RelationStatus.ACCEPT.value,
            relation_type=body.relation,
        )
        return standard_response(
            message="delete relation", http_status=status.HTTP_200_OK
        )


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


@api_view(["GET"])
@validate_token(
    roles=[UserRole.USER], validate_type=UserTokenType.ACCESS, view_type="function"
)
def get_specific_letter(
    request,
    letter_id: str,
    token_payload: UserTokenPayload,
):
    user_letter_box_service = UserLetterBoxService()
    user_token_manager = UserTokenManager()
    current_user = user_token_manager.get_current_user(user_payload_vo=token_payload)
    letter = user_letter_box_service.fetch_letter(
        letter_id=letter_id, user_id=current_user.id
    )

    if letter is None:
        return standard_response(
            message="no letter",
            data="",
            http_status=status.HTTP_200_OK,
        )

    return standard_response(
        message="fetch letter", data=letter, http_status=status.HTTP_200_OK
    )


@api_view(["GET"])
@validate_token(
    roles=[UserRole.USER], validate_type=UserTokenType.ACCESS, view_type="function"
)
def get_received_letters(
    request,
    token_payload: UserTokenPayload,
):
    user_letter_box_service = UserLetterBoxService()
    user_token_manager = UserTokenManager()
    current_user = user_token_manager.get_current_user(user_payload_vo=token_payload)
    letters_data = user_letter_box_service.fetch_received_letter(
        user_id=current_user.id
    )

    if letters_data is None:
        return standard_response(
            message="letter box is empty",
            data=letters_data,
            http_status=status.HTTP_200_OK,
        )
    return standard_response(
        message="fetch received letters",
        data=letters_data,
        http_status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@validate_token(
    roles=[UserRole.USER], validate_type=UserTokenType.ACCESS, view_type="function"
)
def get_sent_letters(
    request,
    token_payload: UserTokenPayload,
):
    user_letter_box_service = UserLetterBoxService()
    user_token_manager = UserTokenManager()
    current_user = user_token_manager.get_current_user(user_payload_vo=token_payload)
    letters_data = user_letter_box_service.fetch_sended_letter(user_id=current_user.id)

    if letters_data is None:
        return standard_response(
            message="letter box is empty",
            data=letters_data,
            http_status=status.HTTP_200_OK,
        )
    return standard_response(
        message="fetch received letters",
        data=letters_data,
        http_status=status.HTTP_200_OK,
    )
