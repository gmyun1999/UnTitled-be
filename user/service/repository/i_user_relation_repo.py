from abc import ABCMeta, abstractmethod

from user.domain.user import UserRelation as UserRelationVo


class IUserRelationRepo(metaclass=ABCMeta):
    class Filter:
        def __init__(
            self,
            relation_type: str | None = None,
            relation_status: str | None = None,
            to_id: str | None = None,
            from_id: str | None = None,
        ):
            self.relation_type = relation_type
            self.relation_status = relation_status
            self.to_id = to_id
            self.from_id = from_id

    @abstractmethod
    def get_bulk(self, filter: Filter) -> list[UserRelationVo] | None:
        pass
