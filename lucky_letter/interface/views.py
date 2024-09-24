from dataclasses import dataclass
from datetime import datetime
from typing import Any

import bleach
from pydantic import BaseModel, Field, field_validator
from rest_framework.views import APIView

from common.interface.validators import validate_body
from lucky_letter.domain.letter import FontType
from lucky_letter.service.letter_service import LetterService
from user.domain.user_role import UserRole
from user.domain.user_token import UserTokenPayload, UserTokenType
from user.interface.validator.user_token_validator import validate_token


class LetterView(APIView):
    def __init__(self):
        self.letter_service = LetterService()

    @dataclass
    class LetterBody(BaseModel):
        to_app_id: str = Field(max_length=36)
        from_app_id: str = Field(max_length=36)
        is_anonymous: bool = Field(default=False)
        writing_pad_id: str = Field(max_length=36)
        envelope_id: str = Field(max_length=36)
        stamp_id: str = Field(max_length=36)
        content: str = Field(max_length=1000)
        title: str = Field(max_length=50)
        font: FontType = Field(max_length=20)
        will_arrive_at: datetime | None = Field(default=None)

        @field_validator("content", "title")
        def sanitize_input(cls, value: str) -> str:
            return bleach.clean(
                value,
                tags=[],
                attributes={},
                strip=True,
            )

    @validate_token(roles=[UserRole.USER], validate_type=UserTokenType.ACCESS)
    @validate_body(LetterBody)
    def post(self, token_payload: UserTokenPayload, body: LetterBody):
        letterVo = self.letter_service.create_letter(
            to_app_id=body.to_app_id,
            from_app_id=body.from_app_id,
            is_anonymous=body.is_anonymous,
            writing_pad_id=body.writing_pad_id,
            envelope_id=body.envelope_id,
            stamp_id=body.stamp_id,
            content=body.content,
            title=body.title,
            font=body.font,
            will_arrive_at=body.will_arrive_at,
        )

        # 뭐 보내주던가 하면될듯.
