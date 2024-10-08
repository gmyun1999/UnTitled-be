import uuid

from notification.domain.notification import Notification as NotificationVo
from user.domain.user import User as UserVo
from user.domain.user_notification import PushMessage
from user.domain.user_token import PushServiceType, UserPushToken
from user.infra.repository.user_push_repo import UserPushRepo
from user.service.push.i_push_server import (
    InvalidTokenError,
    IPushServer,
    UnregisterAppError,
)
from user.service.push.push_server_factory import PushServerFactory
from user.service.repository.i_user_push_repo import IUserPushRepo


class UserPushService:
    def __init__(self) -> None:
        self.push_service_factory = PushServerFactory()
        self.user_push_repo: IUserPushRepo = UserPushRepo()

    def get_push_token(self, user: UserVo) -> str | None:
        user_push_token = self.user_push_repo.get_token(user=user)
        if user_push_token is not None:
            return user_push_token.token

        return None

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
