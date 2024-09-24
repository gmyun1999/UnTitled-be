from dataclasses import dataclass
from typing import Literal

from django.http import HttpRequest, JsonResponse
from pydantic import BaseModel
from rest_framework import status
from rest_framework.views import APIView

from common.interface.exceptions import NotFound
from common.interface.validators import validate_query_params
from common.service.token.i_token_manager import ITokenManager
from user.domain.user import RelationStatus, RelationType, User
from user.domain.user_role import UserRole
from user.domain.user_token import UserTokenPayload, UserTokenType
from user.infra.token.user_token_manager import UserTokenManager
from user.interface.validator.user_token_validator import validate_token
from user.service.user_service import UserRelationService, UserService


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

    @validate_token(roles=[UserRole.USER], validate_type=UserTokenType.ACCESS)
    @validate_query_params(GetRelationParams)
    def get(
        self,
        request: HttpRequest,
        token_payload: UserTokenPayload,
        params: GetRelationParams,
    ):
        user = self.user_token_manager.get_current_user(user_payload_vo=token_payload)

        if user is None:
            return JsonResponse(data={}, status=status.HTTP_400_BAD_REQUEST)

        user_relation = self.user_relation_service.get_relations(
            user_id=user.id,
            relation_status=params.status,
            relation_type=params.relation,
        )
        data: dict = {"relation": user_relation}
        return JsonResponse(data=data, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    def __init__(self):
        self.user_service = UserService()

    @validate_token(
        roles=[UserRole.USER, UserRole.ADMIN], validate_type=UserTokenType.REFRESH
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

        token: dict = self.user_service.create_access_token(user_id=user_id)

        return JsonResponse(status=status.HTTP_200_OK, data=token)
