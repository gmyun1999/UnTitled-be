from common.service.token.i_token_manager import ITokenManager
from common.utils.exceptions import NotFound
from user.domain.user import RelationStatus, RelationType
from user.domain.user import User as UserVo
from user.domain.user import UserRelation as UserRelationVo
from user.infra.repository.user_relation_repo import UserRelationRepo
from user.infra.repository.user_repo import UserRepo
from user.infra.token.user_token_manager import UserTokenManager
from user.service.repository.i_user_relation_repo import IUserRelationRepo
from user.service.repository.i_user_repo import IUserRepo


class UserService:
    def __init__(self):
        # TODO: DI 적용
        self.user_token_manager: ITokenManager = UserTokenManager()
        self.user_repo: IUserRepo = UserRepo()

    def get_me(self, user_id: str | None = None, app_id: str | None = None) -> UserVo:
        user_filter = self.user_repo.Filter(user_id=user_id, app_id=app_id)
        user_vo = self.user_repo.get_user(filter=user_filter)

        if user_vo is None:
            raise NotFound

        return user_vo

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
        """
        return self.user_repo.create(user_vo=user)

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


class UserRelationService:
    def __init__(self) -> None:
        # TODO: Di 적용
        self.user_relation: IUserRelationRepo = UserRelationRepo()

    def get_relations(
        self,
        user_id: str,
        relation_status: str | None = None,
        relation_type: str | None = None,
    ) -> list[dict[str, str]] | None:
        """
        관계 정보를 가져오는 함수.
        """
        relation_filter = self.user_relation.Filter(
            relation_status=relation_status,
            relation_type=relation_type,
            user_id=user_id,
        )
        return self.user_relation.fetch_relations_with_user(
            filter=relation_filter,
            exclude_fields={
                UserRelationVo.FIELD_ID: [],
                UserRelationVo.FIELD_CREATED_AT: [],
                UserRelationVo.FIELD_UPDATED_AT: [],
                UserRelationVo.FIELD_TO_ID: [
                    UserVo.FIELD_ID,
                    UserVo.FIELD_CREATED_AT,
                    UserVo.FIELD_UPDATED_AT,
                ],
                UserRelationVo.FIELD_FROM_ID: [
                    UserVo.FIELD_ID,
                    UserVo.FIELD_CREATED_AT,
                    UserVo.FIELD_UPDATED_AT,
                ],
            },
        )
