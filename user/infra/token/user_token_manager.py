from datetime import datetime, timedelta

import jwt

from common.service.token.i_token_manager import ITokenManager
from letter import settings
from user.domain.user import User as UserVo
from user.domain.user_role import UserRole
from user.domain.user_token import UserTokenExp, UserTokenPayload, UserTokenType
from user.infra.repository.user_repo import UserRepo
from user.service.repository.i_user_repo import IUserRepo


class UserTokenManager(ITokenManager):
    JWT_ALGORITHM = "HS512"
    JWT_SECRET = settings.JWT_SECRET

    def __init__(self) -> None:
        super().__init__()
        # TODO: DI 적용
        self.user_repo: IUserRepo = UserRepo()

    def get_current_user(self, user_payload_vo: UserTokenPayload) -> UserVo | None:
        user_id = user_payload_vo.user_id
        admin_id = user_payload_vo.admin_id

        if user_id:
            user_id = user_id
        if admin_id:
            user_id = admin_id

        user_filter = self.user_repo.Filter(user_id=user_id)
        user: UserVo | None = self.user_repo.get_user(filter=user_filter)

        return user

    def create_admin_access_token(self, admin_id: str) -> str:
        payload = self._create_user_token_payload(
            admin_id=admin_id,
            role=UserRole.ADMIN,
            type=UserTokenType.ACCESS,
            seconds=UserTokenExp.ACCESS_EXP,
        )
        return self._create_user_token(user_payload_vo=payload)

    def create_admin_refresh_token(self, admin_id: str) -> str:
        payload = self._create_user_token_payload(
            admin_id=admin_id,
            role=UserRole.ADMIN,
            type=UserTokenType.REFRESH,
            seconds=UserTokenExp.REFRESH_EXP,
        )
        return self._create_user_token(user_payload_vo=payload)

    def create_user_access_token(self, user_id: str) -> str:
        payload = self._create_user_token_payload(
            user_id=user_id,
            role=UserRole.USER,
            type=UserTokenType.ACCESS,
            seconds=UserTokenExp.ACCESS_EXP,
        )
        return self._create_user_token(user_payload_vo=payload)

    def create_user_refresh_token(self, user_id: str) -> str:
        payload = self._create_user_token_payload(
            user_id=user_id,
            role=UserRole.USER,
            type=UserTokenType.REFRESH,
            seconds=UserTokenExp.REFRESH_EXP,
        )
        return self._create_user_token(user_payload_vo=payload)

    def _create_user_token_payload(
        self,
        user_id: str | None = None,
        admin_id: str | None = None,
        role: UserRole = UserRole.USER,
        type: str = UserTokenType.ACCESS,
        seconds: int = UserTokenExp.ACCESS_EXP,
    ) -> UserTokenPayload:
        return UserTokenPayload(
            admin_id=admin_id,
            user_id=user_id,
            role=role,
            type=type,
            exp=int((datetime.now() + timedelta(seconds=seconds)).timestamp()),  # 만료시간
            iat=int(datetime.now().timestamp()),  # 발급시간
        )

    def _create_user_token(self, user_payload_vo: UserTokenPayload) -> str:
        payload = user_payload_vo.to_dto()
        jwt_token = jwt.encode(payload, self.JWT_SECRET, self.JWT_ALGORITHM)

        return jwt_token
