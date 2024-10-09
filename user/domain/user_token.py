import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum, IntEnum, StrEnum
from typing import Any, Type

from arrow import Arrow
from dacite import Config, from_dict

from common.domain import Domain
from common.utils.base import remove_none


class UserTokenType(StrEnum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


class UserTokenExp(IntEnum):
    ACCESS_EXP = 86_400  # 24시간
    REFRESH_EXP = 5_184_000  # 2달


@dataclass
class UserTokenPayload:
    FIELD_ADMIN_ID = "admin_id"
    FIELD_USER_ID = "user_id"
    FIELD_TYPE = "type"
    FIELD_ROLE = "role"
    FIELD_EXP = "exp"
    FIELD_IAT = "iat"

    admin_id: str | None
    user_id: str | None
    type: str
    role: str
    exp: int  # 만료시간
    iat: int  # 발급시간

    @classmethod
    def from_dict(cls: Type, dto: dict[str, Any]):  # 객체로 변환
        return from_dict(
            data_class=cls,
            data=dto,
            config=Config(cast=[Enum, Arrow]),
        )

    def to_dict(self, excludes: list[str] = []) -> dict[str, Any]:  # dict로 변환
        dto = remove_none(json.dumps(asdict(self), default=str))
        if excludes:
            return {key: value for key, value in dto.items() if key not in excludes}
        else:
            return dto


class PushServiceType(StrEnum):
    FCM = "FCM"


@dataclass
class UserPushToken(Domain):
    id: str
    user_id: str
    push_service: PushServiceType
    token: str
    created_at: str | None = None
