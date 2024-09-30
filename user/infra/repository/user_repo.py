from django.db import DatabaseError

from user.domain.user import User as UserVo
from user.infra.models.serializer import UserSerializer
from user.infra.models.user import User
from user.service.repository.i_user_repo import IUserRepo


class UserRepo(IUserRepo):
    def get_user(self, filter: IUserRepo.Filter) -> UserVo | None:
        try:
            user = User.objects.all()
            if filter.user_id:
                user = user.get(id=filter.user_id)
            if filter.app_id:
                user = user.get(app_id=filter.app_id)

            serializer = UserSerializer(user)
            user_dict = serializer.data
            return UserVo.from_dict(dto=user_dict)

        except User.DoesNotExist:
            return None

    def get_bulk(self):
        pass

    def create(self, user_vo: UserVo) -> UserVo:
        serializer = UserSerializer(data=user_vo.to_dict())

        if serializer.is_valid():
            serializer.save()

            return user_vo.from_dict(serializer.data)
        else:
            raise DatabaseError(serializer.errors)
