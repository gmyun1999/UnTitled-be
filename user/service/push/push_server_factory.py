from user.domain.user_token import PushServiceType
from user.infra.push.fcm import FCM
from user.service.push.i_push_server import PushServer


class PushServerFactory:
    def create(self, push_service_type: PushServiceType) -> PushServer:
        if push_service_type == PushServiceType.FCM:
            return FCM()
