from django.db import DatabaseError

from user.domain.user import User as UserVo
from user.domain.user_token import UserPushToken as UserPushTokenVo
from user.infra.models.serializer import UserPushTokenSerializer
from user.infra.models.user_model import UserPushToken
from user.service.repository.i_user_push_repo import IUserPushRepo


class UserPushRepo(IUserPushRepo):
    def get_token(self, user: UserVo) -> UserPushTokenVo:
        user_id = user.id
        user_psuh_token = UserPushToken.objects.get(user_id=user_id)
        serializer = UserPushTokenSerializer(user_psuh_token)
        dicted = serializer.data
        return UserPushTokenVo.from_dict(dicted)

    def save_push_token(self, user_push_token_vo: UserPushTokenVo) -> UserPushTokenVo:
        dicted = user_push_token_vo.to_dict()
        serializer = UserPushTokenSerializer(data=dicted)
        if serializer.is_valid():
            serializer.save()
            return user_push_token_vo
        else:
            raise DatabaseError(serializer.errors)
