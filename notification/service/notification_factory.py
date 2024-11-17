from types import SimpleNamespace

from lucky_letter.domain.letter import Letter
from notification.domain.notification import NotificationRelatedDomain, NotificationType
from user.domain.user import User as UserVo
from user.domain.user import UserRelation
from user.infra.repository.user_repo import UserRepo
from user.service.repository.i_user_repo import IUserRepo


class TemplateNotFoundError(Exception):
    def __init__(self, notification_type: NotificationType):
        super().__init__(
            f"No template found for notification type: {notification_type}"
        )
        self.notification_type = notification_type


class NotificationTemplateResponse:
    def __init__(
        self,
        title: str,
        message: str,
        related_domain: NotificationRelatedDomain | None,
        target_users: list[UserVo] | None = None,
    ):
        self.title = title
        self.message = message
        self.target_users = target_users
        self.related_domain = related_domain


class NotificationTemplateFactory:
    def __init__(self):
        self.user_repo: IUserRepo = UserRepo()

    def get_template(
        self, notification_type: NotificationType, related_object: object = None
    ) -> NotificationTemplateResponse:
        """
        알맞은 title과 message를 반환

        함수이름 무조건
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        _create_{notification_type}_template 으로 추가할것!!!!!!!!!!!
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """
        factory_method_name = f"_create_{notification_type.value.lower()}_template"
        if not hasattr(self, factory_method_name):
            raise TemplateNotFoundError(notification_type)

        factory_method = getattr(self, factory_method_name)
        return factory_method(related_object)

    def _create_system_template(
        self, related_object: object
    ) -> NotificationTemplateResponse:
        return NotificationTemplateResponse(
            title="시스템 알림", message="예시: 시스템에서 중요한 업데이트가 있었습니다.", related_domain=None
        )

    def _create_advertisement_template(
        self, related_object: object
    ) -> NotificationTemplateResponse:
        return NotificationTemplateResponse(
            title="광고", message="예시: 특별 할인 이벤트가 시작되었습니다!", related_domain=None
        )

    def _create_friend_request_template(
        self, related_object: UserRelation
    ) -> NotificationTemplateResponse:
        if not isinstance(related_object, UserRelation):
            raise ValueError(
                "related_object must be an instance of UserRelation for FRIEND_REQUEST type."
            )

        from_id_filter = self.user_repo.Filter(user_id=related_object.from_id)
        to_id_filter = self.user_repo.Filter(user_id=related_object.to_id)
        from_user = self.user_repo.get_user(filter=from_id_filter)
        if from_user is None:
            raise ValueError("from_user cannot be None.")

        to_user = self.user_repo.get_user(filter=to_id_filter)
        if to_user is None:
            raise ValueError("to_user cannot be None.")

        return NotificationTemplateResponse(
            title="친구 요청",
            message=f"{from_user.name}님이 {to_user.name}님에게 친구 요청을 보냈습니다.",
            target_users=[to_user],
            related_domain=NotificationRelatedDomain.UserRelation,
        )

    def _create_received_letter_template(
        self, related_object: Letter
    ) -> NotificationTemplateResponse:
        if not isinstance(related_object, Letter):
            raise ValueError(
                "related_object must be an instance of Letter for RECEIVED_LETTER type."
            )

        from_id_filter = self.user_repo.Filter(user_id=related_object.from_user_id)
        to_id_filter = self.user_repo.Filter(user_id=related_object.to_user_id)
        from_user = self.user_repo.get_user(filter=from_id_filter)
        if from_user is None:
            raise ValueError("from_user cannot be None.")

        to_user = self.user_repo.get_user(filter=to_id_filter)
        if to_user is None:
            raise ValueError("to_user cannot be None.")

        return NotificationTemplateResponse(
            title="새로운 편지 도착",
            message=f"{from_user.name}님으로부터 '{related_object.title}' 제목의 새로운 편지가 도착했습니다.",
            target_users=[to_user],
            related_domain=NotificationRelatedDomain.Letter,
        )

    def _create_default_template(
        self, related_object: object
    ) -> NotificationTemplateResponse:
        return NotificationTemplateResponse(
            title="알림", message="새로운 알림이 도착했습니다.", related_domain=None
        )

    # def _create_sent_letter_template(self, related_object: Letter) -> dict[str, str]:

    #     if not isinstance(related_object, Letter):
    #         raise ValueError("related_object must be an instance of Letter for SENT_LETTER type.")

    #     to_id_filter = self.user_repo.Filter(user_id=related_object.to_user_id)
    #     to_user = self.user_repo.get_user(filter=to_id_filter) or SimpleNamespace(name="unKnown")

    #     return {
    #         "title": "편지 발송 완료",
    #         "message": f"{to_user.name}님에게 '{related_object.title}' 제목의 편지를 성공적으로 보냈습니다."
    #     }
