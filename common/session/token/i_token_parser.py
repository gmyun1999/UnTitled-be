from abc import ABCMeta, abstractmethod
from typing import Any


class ITokenParser(metaclass=ABCMeta):
    @abstractmethod
    def decode_token(self, token: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def check_token(self, token: str, allowed_roles: list[int], validate_type: str):
        pass
