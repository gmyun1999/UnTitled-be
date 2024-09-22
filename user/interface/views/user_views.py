from dataclasses import dataclass
from typing import Literal

from django.http import HttpRequest, JsonResponse
from pydantic import BaseModel
from rest_framework import status
from rest_framework.views import APIView

from common.interface.validators import validate_query_params
from user.domain.user import RelationStatus, RelationType, User
from user.domain.user_role import UserRole
from user.domain.user_token import UserTokenPayload, UserTokenType
from user.interface.validator.user_token_validator import validate_token
from user.service.user_service import UserRelationService, UserService


class UserRelationView(APIView):
    def __init__(self):
        self.user_relation_service = UserRelationService()
        self.user_service = UserService()

    @dataclass
    class GetRelationParams(BaseModel):
        relation: Literal[RelationType.FRIEND] | None = None
        status: Literal[
            RelationStatus.PENDING, RelationStatus.REJECT, RelationStatus.ACCEPT
        ] | None = None

    @validate_query_params(GetRelationParams)
    def get(self, request: HttpRequest, app_id: str, params: GetRelationParams):
        # TODO: token validator 넣어서 자기 자신만 볼수있게 권한 걸어야함.
        user: User = self.user_service.get_me(app_id=app_id)
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
