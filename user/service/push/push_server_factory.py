from user.domain.user_token import PushServiceType
from user.infra.push.fcm import FCM
from user.service.push.i_push_server import IPushServer


class PushServerFactory:
    def create(self, push_service_type: PushServiceType) -> IPushServer:
        if push_service_type == PushServiceType.FCM:
            return FCM()
