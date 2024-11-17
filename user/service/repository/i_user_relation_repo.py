from abc import ABCMeta, abstractmethod

from user.domain.user import RelationStatus, RelationType
from user.domain.user import UserRelation as UserRelationVo


class IUserRelationRepo(metaclass=ABCMeta):
    class Filter:
        def __init__(
            self,
            relation_type: str | None = None,
            relation_status: str | None = None,
            to_id: str | None = None,
            from_id: str | None = None,
            user_id: str | None = None,
        ):
            self.relation_type = relation_type
            self.relation_status = relation_status
            self.to_id = to_id
            self.from_id = from_id
            self.user_id = user_id

    @abstractmethod
    def check_friend_request_or_friend(self, to_id: str, from_id: str) -> bool:
        pass

    @abstractmethod
    def check_exist(self, filter: Filter) -> bool:
        pass

    @abstractmethod
    def get_one(self, filter: Filter) -> UserRelationVo | None:
        pass

    @abstractmethod
    def get_bulk(self, filter: Filter) -> list[dict[str, str]] | None:
        pass

    @abstractmethod
    def fetch_relations_with_user(
        self, filter: Filter, exclude_fields: dict[str, list[str]] | None = None
    ) -> list[dict[str, str]]:
        pass

    @abstractmethod
    def create(self, UserRelation_vo: UserRelationVo) -> UserRelationVo:
        """
        관계를 새로 생성함.
        """
        pass

    @abstractmethod
    def update(self, existed_user_relation_id: str, filter: Filter) -> UserRelationVo:
        """
        filter 에 있는 필드만 update 시킴.
        """
        pass

    @abstractmethod
    def delete_friendship(
        self,
        to_id: str,
        from_id: str,
        relation_type: str = RelationType.FRIEND.value,
        relation_status: str = RelationStatus.ACCEPT.value,
    ) -> int:
        pass
