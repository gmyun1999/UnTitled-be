from abc import ABCMeta, abstractmethod


class PushServer(metaclass=ABCMeta):
    @abstractmethod
    def validate_token(self, token: str):
        pass

    @abstractmethod
    def send_push_msg(self, message, token: str):
        pass
