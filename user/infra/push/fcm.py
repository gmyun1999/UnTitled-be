from user.service.push.i_push_server import PushServer


class FCM(PushServer):
    def validate_token(self, token: str):
        pass

    def send_push_msg(self, message, token: str):
        pass
