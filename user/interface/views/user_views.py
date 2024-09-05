from django.http import HttpRequest, JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from user.domain.user_role import UserRole
from user.domain.user_token import UserTokenPayload, UserTokenType
from user.interface.validator.user_token_validator import validate_token
from user.service.user_service import UserService

class OAuthLoginView(APIView):
    pass

class UserView(APIView):
    pass

class RefreshTokenView(APIView):
    def __init__(self):
        self.user_service = UserService()
        
    @validate_token(
        roles=[UserRole.USER, UserRole.ADMIN],
        validate_type=UserTokenType.REFRESH
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
            
        token: str = self.user_service.create_access_token(user_id=user_id)

        return JsonResponse(status=status.HTTP_200_OK, data=token)
