import uuid

from notification.domain.notification import NotificationType
from notification.service.notification_service import NotificationService
from user.domain.user import RelationStatus, RelationType
from user.domain.user import User as UserVo
from user.domain.user import UserRelation as UserRelationVo
from user.infra.repository.user_relation_repo import UserRelationRepo
from user.service.repository.i_user_relation_repo import IUserRelationRepo


class UserRelationService:
    def __init__(self) -> None:
        # TODO: Di 적용
        self.user_relation_repo: IUserRelationRepo = UserRelationRepo()

        self.notification_service = NotificationService()

    def get_relation_by_id(
        self,
        relation_id: str,
    ):
        return self.user_relation_repo.fetch_relations_with_user(
            filter=self.user_relation_repo.Filter(id=relation_id),
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

    def get_relations(
        self,
        user_id: str,
        relation_status: str | None = None,
        relation_type: str | None = None,
    ) -> list[dict[str, str]]:
        """
        관계 정보를 가져오는 함수.
        """
        relation_filter = self.user_relation_repo.Filter(
            relation_status=relation_status,
            relation_type=relation_type,
            user_id=user_id,
        )
        return self.user_relation_repo.fetch_relations_with_user(
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

    def create_relation(
        self,
        to_id: str,
        from_id: str,
        relation_status: RelationStatus,
        relation_type: RelationType = RelationType.FRIEND,
    ) -> UserRelationVo | None:
        user_relation_vo = UserRelationVo(
            id=str(uuid.uuid4()),
            to_id=to_id,
            from_id=from_id,
            relation_status=relation_status,
            relation_type=relation_type,
        )

        is_exist = self.user_relation_repo.check_friend_request_or_friend(
            to_id=to_id, from_id=from_id
        )

        if is_exist:
            return None

        user_relation = self.user_relation_repo.create(UserRelation_vo=user_relation_vo)

        # 친구요청의 경우 알림 발송
        if relation_type == RelationType.FRIEND:
            self.notification_service.create_notification(
                notification_type=NotificationType.FRIEND_REQUEST,
                related_object=user_relation,
            )

        return user_relation

    def update_my_relation(
        self,
        my_id: str,
        requested_id: str,
        relation_status: RelationStatus,
        relation_type: RelationType = RelationType.FRIEND,
    ) -> UserRelationVo | None:
        filter = self.user_relation_repo.Filter(
            to_id=my_id,
            from_id=requested_id,
            relation_status=RelationStatus.PENDING,
            relation_type=RelationType.FRIEND,
        )
        user_relation = self.user_relation_repo.get_one(filter=filter)

        if user_relation is None:
            return None

        update_filter = self.user_relation_repo.Filter(
            to_id=my_id,
            from_id=requested_id,
            relation_status=relation_status,
            relation_type=relation_type,
        )
        return self.user_relation_repo.update(
            existed_user_relation_id=user_relation.id, filter=update_filter
        )

    def delete_my_relation(
        self,
        my_id: str,
        to_id: str,
        relation_type: str = RelationType.FRIEND.value,
        relation_status: str = RelationStatus.ACCEPT.value,
    ):
        return self.user_relation_repo.delete_friendship(
            to_id=my_id,
            from_id=to_id,
            relation_type=relation_type,
            relation_status=relation_status,
        )

    def delete_my_relation_bulk(
        self,
        my_id: str,
        relation_type: str = RelationType.FRIEND.value,
        relation_status: str = RelationStatus.ACCEPT.value,
    ):
        return self.user_relation_repo.delete_all_friendships_for_user(
            my_id=my_id,
            relation_type=relation_type,
            relation_status=relation_status,
        )
