from abc import ABCMeta, abstractmethod


class InvalidTokenError(Exception):
    """
    token valid 시 잘못된 토큰
    """

    pass


class UnregisterAppError(Exception):
    """
    시용자가 기기에서 앱을 삭제했을때 혹은 토큰만료
    """

    pass


class IPushServer(metaclass=ABCMeta):
    @abstractmethod
    def validate_token(self, token: str):
        pass

    @abstractmethod
    def send_push_msg(self, message, token: str):
        pass
