from common.service.token.i_token_manager import ITokenManager
from user.domain.user import User as UserVo
from user.infra.repository.user_repo import UserRepo
from user.infra.token.user_token_manager import UserTokenManager
from user.service.repository.i_user_repo import IUserRepo
from user.service.user_notification_service import UserNotificationService


class UserService:
    def __init__(self):
        # TODO: DI 적용
        self.user_token_manager: ITokenManager = UserTokenManager()
        self.user_repo: IUserRepo = UserRepo()

        self.user_notification_setting_service = UserNotificationService()

    def get_user_by_app_id(self, app_id: str) -> UserVo | None:
        filter = self.user_repo.Filter(app_id=app_id)
        return self.user_repo.get_user(filter=filter)

    def get_users_by_app_ids(self, app_ids: list[str]) -> list[UserVo]:
        filter = self.user_repo.Filter(app_ids=app_ids)
        return self.user_repo.get_users_by_app_ids(filter=filter)

    def check_duplicate_app_id(self, app_id: str) -> bool:
        """
        이미 있으면 true, 없으면 false를 반환.
        중복 여부를 return 한다.
        """

        filter = self.user_repo.Filter(app_id=app_id)
        user = self.user_repo.get_user(filter=filter)
        if user is not None:
            return True
        if user is None:
            return False

    def create_access_token(self, user_id: str) -> dict:
        return {"access": self.user_token_manager.create_user_access_token(user_id)}

    def create_user(self, user: UserVo) -> UserVo:
        """
        그냥 user 만든다음에 db에 밀어넣으면됨.

        user 별 기본 알림 세팅 초기화
        """
        user = self.user_repo.create(user_vo=user)

        self.user_notification_setting_service.init_notification_setting(user_vo=user)
        return user

    def create_user_token(self, user_id: str) -> dict[str, str]:
        """
        access, refresh 모두 만들어서 돌려줌.
        return :  {
            access: access_token,
            refresh: refresh_token
        }
        """
        return {
            "access": self.user_token_manager.create_user_access_token(user_id),
            "refresh": self.user_token_manager.create_user_refresh_token(user_id),
        }

    def delete_user(self, user: UserVo) -> None:
        self.user_repo.delete(user_vo=user)
