from django.db.models import Q

from user.infra.models.serializer import (
    UserJoinRelationSerializer,
    UserRelationSerializer,
)
from user.infra.models.user import UserRelation
from user.service.repository.i_user_relation_repo import IUserRelationRepo


class UserRelationRepo(IUserRelationRepo):
    def get_bulk(self, filter: IUserRelationRepo.Filter) -> list[dict[str, str]] | None:
        """
        relation dict으로 이루어진 list 를 반환한다.
        dict은 relation 모델을 dict으로 변환한거
        """

        user_relation = UserRelation.object.all()
        if filter.relation_type:
            user_relation = user_relation.filter(relation_type=filter.relation_type)
        if filter.relation_status:
            user_relation = user_relation.filter(relation_status=filter.relation_status)
        if filter.to_id:
            user_relation = user_relation.filter(to_id=filter.to_id)
        if filter.from_id:
            user_relation = user_relation.filter(from_id=filter.from_id)
        if filter.user_id:
            user_relation = user_relation.filter(
                Q(from_id__id=filter.user_id) | Q(to_id__id=filter.user_id)
            )

        serializer = UserRelationSerializer(user_relation, many=True)
        user_relations = serializer.data
        if user_relations:
            return user_relations

        return None

    def fetch_relations_with_user(
        self,
        filter: IUserRelationRepo.Filter,
        exclude_fields: dict[str, list[str]] | None = None,
    ) -> list[dict[str, str]] | None:
        """
        User 모델과 UserRelation을 조인하여 필터링된 결과를 반환.
        """

        queryset = UserRelation.objects.select_related("to_id", "from_id")

        if filter.to_id:
            queryset = queryset.filter(to_id__id=filter.to_id)
        if filter.from_id:
            queryset = queryset.filter(from_id__id=filter.from_id)
        if filter.relation_type:
            queryset = queryset.filter(relation_type=filter.relation_type)
        if filter.relation_status:
            queryset = queryset.filter(relation_status=filter.relation_status)
        if filter.user_id:
            queryset = queryset.filter(
                Q(from_id__id=filter.user_id) | Q(to_id__id=filter.user_id)
            )

        serializer = UserJoinRelationSerializer(
            queryset, many=True, exclude_fields=exclude_fields or {}
        )

        return serializer.data if serializer.data else None
