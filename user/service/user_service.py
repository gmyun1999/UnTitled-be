import uuid
from datetime import datetime
from typing import Any

from common.service.token.i_token_manager import ITokenManager
from notification.domain.notification import Notification as NotificationVo
from notification.domain.notification import NotificationType
from user.domain.user import RelationStatus, RelationType
from user.domain.user import User as UserVo
from user.domain.user import UserRelation as UserRelationVo
from user.domain.user_letter_box import UserLetterBox, UserLetterBoxType
from user.domain.user_notification import (
    PushMessage,
    UserNotification,
    UserNotificationSetting,
)
from user.domain.user_token import PushServiceType, UserPushToken
from user.infra.repository.user_letter_box import UserLetterBoxRepo
from user.infra.repository.user_notification_repo import (
    UserNotificationRepo,
    UserNotificationSettingRepo,
)
from user.infra.repository.user_push_repo import UserPushRepo
from user.infra.repository.user_relation_repo import UserRelationRepo
from user.infra.repository.user_repo import UserRepo
from user.infra.token.user_token_manager import UserTokenManager
from user.service.push.i_push_server import (
    InvalidTokenError,
    IPushServer,
    UnregisterAppError,
)
from user.service.push.push_server_factory import PushServerFactory
from user.service.repository.i_user_letter_box import IUserLetterBoxRepo
from user.service.repository.i_user_notification_repo import (
    IUserNotificationRepo,
    IUserNotificationSettingRepo,
)
from user.service.repository.i_user_push_repo import IUserPushRepo
from user.service.repository.i_user_relation_repo import IUserRelationRepo
from user.service.repository.i_user_repo import IUserRepo


class UserService:
    def __init__(self):
        # TODO: DI 적용
        self.user_token_manager: ITokenManager = UserTokenManager()
        self.user_repo: IUserRepo = UserRepo()

    def get_user_by_app_id(self, app_id: str) -> UserVo | None:
        filter = self.user_repo.Filter(app_id=app_id)
        return self.user_repo.get_user(filter=filter)

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

    def delete_user(self, user: UserVo) -> None:
        self.user_repo.delete(user_vo=user)


class UserRelationService:
    def __init__(self) -> None:
        # TODO: Di 적용
        self.user_relation_repo: IUserRelationRepo = UserRelationRepo()

    def get_relations(
        self,
        user_id: str,
        relation_status: str | None = None,
        relation_type: str | None = None,
    ) -> list[dict[str, str]] | None:
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

        return self.user_relation_repo.create(UserRelation_vo=user_relation_vo)

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


class UserLetterBoxService:
    def __init__(self):
        self.letter_box_repo: IUserLetterBoxRepo = UserLetterBoxRepo()

    def fetch_letter(self, letter_id: str, user_id: str) -> dict[str, Any] | None:
        return self.letter_box_repo.get_my_letter(letter_id=letter_id, user_id=user_id)

    def fetch_sended_letter(self, user_id: str) -> list[dict[str, Any]] | None:
        return self.letter_box_repo.fetch_my_letters(
            user_id=user_id, letter_type=UserLetterBoxType.SENT
        )

    def fetch_received_letter(self, user_id: str) -> list[dict[str, Any]] | None:
        return self.letter_box_repo.fetch_my_letters(
            user_id=user_id, letter_type=UserLetterBoxType.RECEIVED
        )

    def store_letter(self, letter_id: str, user_id: str, type: UserLetterBoxType):
        user_letter_box_vo = UserLetterBox(
            id=str(uuid.uuid4()),
            user_id=user_id,
            letter_id=letter_id,
            type=type,
            is_read=False,
        )
        return self.letter_box_repo.store_letter_in_letter_box(user_letter_box_vo)

    def delete_sended_letter(self, letter_id: str, user_id: str):
        pass

    def delete_received_letter(self, letter_id: str, user_id: str):
        pass


class UserNotificationService:
    def __init__(self) -> None:
        # TODO: DI 적용
        self.user_notification_repo: IUserNotificationRepo = UserNotificationRepo()
        self.user_notification_setting_repo: IUserNotificationSettingRepo = (
            UserNotificationSettingRepo()
        )
        self.user_push_service = UserPushService()

    def get_my_notification_setting(self, user_vo: UserVo):
        """
        내가 세팅해놓은 알림 상태 가져오기
        """
        filter = self.user_notification_setting_repo.Filter(user_id=user_vo.id)
        return self.user_notification_setting_repo.get_user_settings(filter=filter)

    def get_my_specific_notification_setting(
        self, user_vo: UserVo, notification_type: NotificationType
    ):
        filter = self.user_notification_setting_repo.Filter(
            user_id=user_vo.id, notification_type=notification_type
        )
        return self.user_notification_setting_repo.get_user_settings(filter=filter)

    def update_my_notification_setting(
        self,
        previous_id: str,
        user_vo: UserVo,
        is_push_allow: bool,
        notification_type: NotificationType | None,
    ):
        """
        내 알림 세팅 수정하기
        """
        filter = self.user_notification_setting_repo.Filter(
            user_id=user_vo.id,
            is_push_allow=is_push_allow,
            notification_type=notification_type,
        )
        return self.user_notification_setting_repo.modify_user_settings(
            existed_user_setting_id=previous_id, filter=filter
        )

    def get_my_notification(self, user_vo: UserVo) -> list[dict[str, Any] | None]:
        """
        내 알림함에 있는 알림들 가져오기
        """
        filter = self.user_notification_repo.Filter(user_id=user_vo.id)
        return self.user_notification_repo.get_user_notification(filter=filter)

    def delete_my_notification(self, my_notification_id: str, is_bulk: bool = False):
        """
        내 알림함에 있는 알림들 지우기
        """
        pass

    def save_user_notification(self, notification_vo: NotificationVo, user_vo: UserVo):
        """
        user와 notification을 이용해서 알림 객체를 저정한다.
        """
        user_notification = UserNotification(
            id=str(uuid.uuid4()),
            user_id=user_vo.id,
            notification_id=notification_vo.id,
            is_read=False,
            delivered_at=datetime.now(),
        )
        return self.user_notification_repo.save_user_notification(
            user_notification_vo=user_notification
        )

    def create_user_notification(
        self, notification_vo: NotificationVo, user_vo: UserVo
    ) -> tuple[PushMessage | None, str]:
        """
        save 시킨다음에 user_notification setting 을 확인한후에 send_push_msg를 호출한다.
        """
        self.save_user_notification(notification_vo=notification_vo, user_vo=user_vo)
        my_setting = self.get_my_specific_notification_setting(
            user_vo=user_vo, notification_type=notification_vo.notification_type
        )[0]

        if my_setting[UserNotificationSetting.FIELD_IS_PUSH_ALLOW] is True:
            msg = self.user_push_service.create_push_message(
                user=user_vo, notification=notification_vo
            )
            token = self.user_push_service.get_push_token(user=user_vo)
            push_msg, result = self.user_push_service.send_push_msg(
                msg=msg, token=token
            )
            return push_msg, result
        return None, "save user notification"


class UserPushService:
    def __init__(self) -> None:
        self.push_service_factory = PushServerFactory()
        self.user_push_repo: IUserPushRepo = UserPushRepo()

    def get_push_token(self, user: UserVo) -> str:
        user_push_token = self.user_push_repo.get_token(user=user)
        return user_push_token.token

    def save_push_service_token(
        self,
        token: str,
        user: UserVo,
        service_type: PushServiceType = PushServiceType.FCM,
    ) -> UserPushToken | None:
        """
        app으로부터 token을 받아서 저장한다.
        token이 invalid 한경우 None을 return
        """

        server = self.push_service_factory.create(push_service_type=service_type)
        if not server.validate_token(token=token):
            return None

        user_push_token = UserPushToken(
            id=str(uuid.uuid4()),
            user_id=user.id,
            push_service=service_type,
            token=token,
        )
        return self.user_push_repo.save_push_token(user_push_token_vo=user_push_token)

    def create_push_message(
        self,
        user: UserVo,
        notification: NotificationVo,
    ) -> PushMessage:
        return PushMessage(
            user_name=user.name,
            title=notification.title,
            body=notification.message,
            notification_type=notification.notification_type,
        )

    def send_push_msg(
        self,
        msg: PushMessage,
        token: str,
        service_type: PushServiceType = PushServiceType.FCM,
    ) -> tuple[PushMessage | None, str]:
        """
        성공하면 msg, 성공 메세지
        실패하면 None, 실패 메세지
        """
        push_server: IPushServer = self.push_service_factory.create(
            push_service_type=service_type
        )
        try:
            push_server.send_push_msg(message=msg, token=token)
            return msg, "send success`"

        except InvalidTokenError:
            return None, "token is invalid"

        except UnregisterAppError:
            return None, "app is not register"
