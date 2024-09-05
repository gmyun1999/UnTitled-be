from common.service.token.i_token_manager import ITokenManager
from user.infra.token.user_token_manager import UserTokenManager


class UserService:
    def __init__(self):
        # TODO: DI 적용
        self.user_token_manager:ITokenManager = UserTokenManager()
        
    def create_access_token(self, user_id: str):
        return self.user_token_manager.create_user_access_token(user_id)
        