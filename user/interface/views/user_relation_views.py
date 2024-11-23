from dataclasses import dataclass
from typing import Literal

from django.http import HttpRequest
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from pydantic import BaseModel, Field
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from common.interface.http_response import standard_response
from common.interface.validators import validate_body, validate_query_params
from common.paging import Paginator
from common.service.token.i_token_manager import ITokenManager
from user.domain.user import RelationStatus, RelationType
from user.domain.user_role import UserRole
from user.domain.user_token import UserTokenPayload, UserTokenType
from user.infra.models.swagger.user_relation.get_user_relation import (
    GetUserRelationResponseSerializer,
    UserRelationResponseSerializer,
)
from user.infra.models.swagger.user_relation.post import (
    ErrorResponseSerializer,
    UserRelationCreateRequestSerializer,
    UserRelationDeleteRequestSerializer,
)
from user.infra.token.user_token_manager import UserTokenManager
from user.interface.validator.user_token_validator import validate_token
from user.service.user_relation_service import UserRelationService
from user.service.user_service import UserService


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
        page: int | None = Field(default=None, ge=1)
        page_size: int | None = Field(default=None, ge=1)

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
        to_app_ids: list[str] = Field()

    @extend_schema(
        summary="사용자 관계 조회",
        description="특정 사용자의 관계 정보 조회",
        responses={200: UserRelationResponseSerializer},
        parameters=[
            OpenApiParameter(
                "relation", OpenApiTypes.STR, description="관계 타입 (FRIEND)"
            ),
            OpenApiParameter(
                "status",
                OpenApiTypes.STR,
                description="관계 상태 (PENDING, REJECT, ACCEPT)",
            ),
            OpenApiParameter("page", OpenApiTypes.INT, description="페이지 번호"),
            OpenApiParameter("page_size", OpenApiTypes.INT, description="페이지 크기"),
        ],
    )
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
        if params.page is None or params.page_size is None:
            return standard_response(
                message="fetch my relationship",
                data=user_relation,
                http_status=status.HTTP_200_OK,
            )

        paged_result = Paginator.paginate(
            items=user_relation,
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
            message="fetch user relation",
            data=response_data,
            http_status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="사용자 관계 생성",
        description="특정 사용자와 새로운 관계를 생성",
        request=UserRelationCreateRequestSerializer,
        responses={
            201: UserRelationResponseSerializer,
            400: OpenApiResponse(
                response=ErrorResponseSerializer, description="잘못된 요청입니다."
            ),
            404: OpenApiResponse(
                response=ErrorResponseSerializer, description="대상 사용자가 존재하지 않습니다."
            ),
            409: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="이미 요청된 관계가 있거나 기존 관계가 존재합니다.",
            ),
        },
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

    @extend_schema(
        summary="사용자 관계 업데이트",
        description="특정 사용자와의 관계를 업데이트 (예: 친구 요청 수락 또는 거절)",
        request=UserRelationCreateRequestSerializer,
        responses={
            200: OpenApiResponse(
                response=UserRelationResponseSerializer,
                description="관계가 성공적으로 업데이트되었습니다.",
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer, description="잘못된 요청입니다."
            ),
            404: OpenApiResponse(
                response=ErrorResponseSerializer, description="대상 사용자가 존재하지 않습니다."
            ),
            409: OpenApiResponse(
                response=ErrorResponseSerializer, description="업데이트할 관계가 존재하지 않습니다."
            ),
        },
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

    @extend_schema(
        summary="사용자 관계 삭제",
        description="""
        특정 사용자와의 관계들을 삭제 . 이유를 모르겠지만 스웨거 request가 생성이안됨.
        {
        "relation" : "FRIEND",
        "to_app_ids": ["app8"]
        } 이게 request body이다., 
        """,
        request=UserRelationDeleteRequestSerializer,
        responses={
            200: OpenApiResponse(
                response=ErrorResponseSerializer, description="관계가 성공적으로 삭제되었습니다."
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer, description="잘못된 요청입니다."
            ),
            404: OpenApiResponse(
                response=ErrorResponseSerializer, description="삭제할 대상 사용자가 존재하지 않습니다."
            ),
        },
    )
    @validate_token(roles=[UserRole.USER], validate_type=UserTokenType.ACCESS)
    @validate_body(DeleteRelationParams)
    def delete(
        self,
        request: HttpRequest,
        token_payload: UserTokenPayload,
        body: DeleteRelationParams,
    ):
        current_user = self.user_token_manager.get_current_user(
            user_payload_vo=token_payload
        )

        to_user_list = self.user_service.get_users_by_app_ids(app_ids=body.to_app_ids)
        for to_user in to_user_list:
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


@extend_schema(
    summary="사용자 관계 가져오기",
    description="relation_id를 이용해서 특정 관계를 가져온다.",
    responses={200: GetUserRelationResponseSerializer},
)
@api_view(["GET"])
@validate_token(
    roles=[UserRole.USER], validate_type=UserTokenType.ACCESS, view_type="function"
)
def get_relation(
    request: HttpRequest, relation_id: str, token_payload: UserTokenPayload
):
    user_relation_service = UserRelationService()
    # TODO: 관련 없는사람의 relation 못보게 막기
    # user_service = UserService()
    # user = self.user_token_manager.get_current_user(user_payload_vo=token_payload)
    user_relation = user_relation_service.get_relation_by_id(relation_id=relation_id)
    if user_relation is None:
        return standard_response(
            message="fetch my relationship",
            data=None,
            http_status=status.HTTP_200_OK,
        )
    return standard_response(
        message="fetch my relationship",
        data=user_relation,
        http_status=status.HTTP_200_OK,
    )
