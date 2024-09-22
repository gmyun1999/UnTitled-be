from django.db import DatabaseError

from user.domain.user import User as UserVo
from user.domain.user import UserRelation as UserRelationVo
from user.infra.models.serializer import UserRelationSerializer, UserSerializer
from user.infra.models.user import UserRelation
from user.service.repository.i_user_relation_repo import IUserRelationRepo


class UserRelationRepo(IUserRelationRepo):
    def get_bulk(self, filter: IUserRelationRepo.Filter) -> list[UserRelationVo] | None:
        user_relation = UserRelation.object.all()
        if filter.relation_type:
            user_relation = user_relation.filter(relation_type=filter.relation_type)
        if filter.relation_status:
            user_relation = user_relation.filter(relation_status=filter.relation_status)
        if filter.to_id:
            user_relation = user_relation.filter(to_id=filter.to_id)
        if filter.from_id:
            user_relation = user_relation.filter(from_id=filter.from_id)

        serializer = UserRelationSerializer(user_relation)
        user_relation_dict = serializer.data

        if user_relation_dict:
            return [item.from_dto(dto=item) for item in user_relation_dict]

        return None
