from dataclasses import dataclass
from typing import Literal

from django.http import HttpRequest
from pydantic import BaseModel, Field
from rest_framework import status
from rest_framework.views import APIView

from common.interface.http_response import standard_response
from common.interface.validators import validate_body, validate_query_params
from common.paging import Paginator
from common.service.token.i_token_manager import ITokenManager
from user.domain.user import RelationStatus, RelationType
from user.domain.user_role import UserRole
from user.domain.user_token import UserTokenPayload, UserTokenType
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
        page: int = Field(default=1, ge=1)
        page_size: int = Field(default=10, ge=1)

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
