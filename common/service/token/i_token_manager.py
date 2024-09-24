from abc import ABCMeta, abstractmethod

from user.domain.user import User
from user.domain.user_token import UserTokenPayload


class ITokenManager(metaclass=ABCMeta):
    @abstractmethod
    def get_current_user(self, user_payload_vo: UserTokenPayload) -> User | None:
        pass

    @abstractmethod
    def create_admin_access_token(self, admin_id: str) -> str:
        pass

    @abstractmethod
    def create_admin_refresh_token(self, admin_id: str) -> str:
        pass

    @abstractmethod
    def create_user_access_token(self, user_id: str) -> str:
        pass

    @abstractmethod
    def create_user_refresh_token(self, user_id: str) -> str:
        pass
