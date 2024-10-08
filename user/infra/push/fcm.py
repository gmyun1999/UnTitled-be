from firebase_admin import messaging
from firebase_admin._messaging_utils import UnregisteredError

from user.domain.user_notification import PushMessage
from user.service.push.i_push_server import (
    InvalidTokenError,
    IPushServer,
    UnregisterAppError,
)


class FCM(IPushServer):
    def validate_token(self, token: str) -> bool:
        message = messaging.Message(token=token)

        # 메시지 전송 시도
        try:
            response = messaging.send(message, dry_run=True)  # token 유효성만 판단
            print("this is valid fcm_token:", response)
            return True

        except Exception as e:
            print("invalid token:", e)
            return False

    def send_push_msg(self, message: PushMessage, token: str):
        if not self.validate_token(token=token):
            raise InvalidTokenError
        message = messaging.Message(
            notification=messaging.Notification(title=message.title, body=message.body),
            token=token,
        )

        try:
            response = messaging.send(message)
            print("Successfully sent message:", response)
        except UnregisteredError:
            raise UnregisterAppError
