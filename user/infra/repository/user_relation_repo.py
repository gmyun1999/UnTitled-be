from django.db import DatabaseError
from django.db.models import Q

from user.domain.user import UserRelation as UserRelationVo
from user.infra.models.serializer import (
    UserJoinRelationSerializer,
    UserRelationSerializer,
)
from user.infra.models.user import UserRelation
from user.service.repository.i_user_relation_repo import IUserRelationRepo


class UserRelationRepo(IUserRelationRepo):
    def check_exist(self, filter: IUserRelationRepo.Filter) -> bool:
        user_relation = UserRelation.objects.all()

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

        return user_relation.exists()

    def get_one(self, filter: IUserRelationRepo.Filter) -> UserRelationVo | None:
        user_relation = UserRelation.objects.all()

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

        query = user_relation.first()
        if query is None:
            return None

        serializer = UserRelationSerializer(query)
        dicted_relation = serializer.data

        return UserRelationVo.from_dict(dicted_relation)

    def get_bulk(self, filter: IUserRelationRepo.Filter) -> list[dict[str, str]] | None:
        """
        relation dict으로 이루어진 list 를 반환한다.
        dict은 relation 모델을 dict으로 변환한거
        """

        user_relation = UserRelation.objects.all()
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

    def create(self, UserRelation_vo: UserRelationVo) -> UserRelationVo:
        dict_user_relation = UserRelation_vo.to_dict()
        serializer = UserRelationSerializer(data=dict_user_relation)
        if serializer.is_valid():
            serializer.save()
            return UserRelation_vo
        else:
            raise DatabaseError(serializer.errors)

    def update(
        self, existed_user_relation_id: str, filter: IUserRelationRepo.Filter
    ) -> UserRelationVo:
        instance = UserRelation.objects.get(id=existed_user_relation_id)
        update_data = {}

        if filter.relation_type:
            update_data[UserRelationVo.FIELD_RELATION_TYPE] = filter.relation_type
        if filter.relation_status:
            update_data[UserRelationVo.FIELD_RELATION_STATUS] = filter.relation_status
        if filter.to_id:
            update_data[UserRelationVo.FIELD_TO_ID] = filter.to_id
        if filter.from_id:
            update_data[UserRelationVo.FIELD_FROM_ID] = filter.from_id

        serializer = UserRelationSerializer(
            instance=instance, data=update_data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            dicted_data = serializer.data
            return UserRelationVo.from_dict(dicted_data)
        else:
            raise DatabaseError(serializer.errors)
