from abc import ABCMeta, abstractmethod

from user.domain.user import User as userVo
from user.domain.user_token import UserPushToken as UserPushTokenVo


class IUserPushRepo(metaclass=ABCMeta):
    @abstractmethod
    def get_token(self, user: userVo) -> UserPushTokenVo:
        pass

    @abstractmethod
    def save_push_token(self, user_push_token_vo: UserPushTokenVo) -> UserPushTokenVo:
        pass
