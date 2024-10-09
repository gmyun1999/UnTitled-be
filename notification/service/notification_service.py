import uuid

from common.domain import Domain
from notification.domain.notification import Notification, NotificationType
from notification.infra.repository.notification_repo import NotificationRepo
from notification.service.notification_factory import (
    NotificationTemplateFactory,
    NotificationTemplateResponse,
)
from notification.service.repository.i_notification_repo import INotificationRepo
from user.infra.repository.user_repo import UserRepo
from user.service.repository.i_user_repo import IUserRepo
from user.service.user_notification_service import UserNotificationService


class NotificationService:
    def __init__(self) -> None:
        self.notification_repo: INotificationRepo = NotificationRepo()
        self.notification_factory = NotificationTemplateFactory()
        self.user_notification_service = UserNotificationService()
        self.user_repo: IUserRepo = UserRepo()

    def create_notification(
        self, notification_type: NotificationType, related_object: Domain
    ):
        template: NotificationTemplateResponse = self.notification_factory.get_template(
            notification_type=notification_type, related_object=related_object
        )

        notification = Notification(
            id=str(uuid.uuid4()),
            title=template.title,
            message=template.message,
            notification_type=notification_type,
            related_domain=template.related_domain,
            related_object_id=related_object.id,
        )

        self.notification_repo.save(notification)

        # user notification에 각자 보내주기.
        if template.target_users is None:
            # 전체발송. 아직 미구현
            # 아마 전체발송의 개념보다는 공통 notification용으로 하나 만들거같음
            pass
        else:
            for user in template.target_users:
                result, msg = self.user_notification_service.create_user_notification(
                    notification_vo=notification, user_vo=user
                )
                if result is None:
                    print(msg)
