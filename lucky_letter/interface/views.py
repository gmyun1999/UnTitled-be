from dataclasses import dataclass

import bleach
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from pydantic import BaseModel, Field, field_validator
from rest_framework import status
from rest_framework.views import APIView

from common.interface.http_response import standard_response
from common.interface.validators import validate_body
from common.service.token.i_token_manager import ITokenManager
from lucky_letter.domain.letter import FontType
from lucky_letter.infra.swagger.letter import LetterBodyRequestSerializer
from lucky_letter.service.letter_service import LetterService
from user.domain.user_role import UserRole
from user.domain.user_token import UserTokenPayload, UserTokenType
from user.infra.models.swagger.user_letter import LetterStandardResponseSerializer
from user.infra.token.user_token_manager import UserTokenManager
from user.interface.validator.user_token_validator import validate_token
from user.service.user_letter_box_service import UserLetterBoxService
from user.service.user_service import UserService


class ReplyLetterView(APIView):
    def __init__(self):
        self.letter_service = LetterService()
        self.user_letter_box_service = UserLetterBoxService()
        self.user_service = UserService()
        # TODO: DI 적용
        self.token_manager: ITokenManager = UserTokenManager()

    @extend_schema(
        summary=" 답장한 letter 가져오기",
        description="letter_box id 가아닌 letter_id를 path param으로 넘긴다",
        responses={200: LetterStandardResponseSerializer},
    )
    @validate_token(roles=[UserRole.USER], validate_type=UserTokenType.ACCESS)
    def get(self, request, letter_id: str, token_payload: UserTokenPayload):
        user = self.token_manager.get_current_user(token_payload)
        letter = self.letter_service.get_letter_by_id(letter_id=letter_id)

        # letter_id가 없을때
        if letter is None:
            return standard_response(
                message="letter_id is not exist",
                data="",
                http_status=status.HTTP_400_BAD_REQUEST,
            )

        # letter_id 를 보낸사람, 혹은 받은 사람이 아닐때
        if letter.to_user_id != user.id and letter.from_user_id != user.id:
            return standard_response(
                message="permission denied",
                data="",
                http_status=status.HTTP_400_BAD_REQUEST,
            )

        letter_vo = self.letter_service.get_reply_letter(target_letter_id=letter_id)
        if letter_vo is None:
            return standard_response(
                message="no reply letter",
                data={},
                http_status=status.HTTP_200_OK,
            )

        return standard_response(
            message="fetch reply letter",
            data=letter_vo.to_dict(),
            http_status=status.HTTP_200_OK,
        )


class LetterView(APIView):
    def __init__(self):
        self.letter_service = LetterService()
        self.user_service = UserService()
        # TODO: DI 적용
        self.token_manager: ITokenManager = UserTokenManager()

    @dataclass
    class LetterBody(BaseModel):
        to_app_id: str = Field(max_length=36)  # 아직은 전체전송 막아두겠음Z
        to_letter_id: str | None = Field(max_length=36, default=None)  # 답장이 아닌경우 None
        is_anonymous: bool = Field(default=False)
        writing_pad_id: str = Field(max_length=36)
        envelope_id: str = Field(max_length=36)
        stamp_id: str = Field(max_length=36)
        content: str = Field(max_length=1000)
        title: str = Field(max_length=50)
        font: FontType = Field(max_length=20)
        will_arrive_at: str | None = Field(default=None)

        @field_validator("content", "title")
        def sanitize_input(cls, value: str) -> str:
            return bleach.clean(
                value,
                tags=[],
                attributes={},
                strip=True,
            )

    @extend_schema(
        summary=" 편지 보내기",
        request=LetterBodyRequestSerializer,
        description="to_letter_id가 없으면 새로운 편지, 있으면 답장",
        responses={200: LetterStandardResponseSerializer},
    )
    @validate_token(roles=[UserRole.USER], validate_type=UserTokenType.ACCESS)
    @validate_body(LetterBody)
    def post(self, request, token_payload: UserTokenPayload, body: LetterBody):
        user = self.token_manager.get_current_user(token_payload)

        # 보내는 사람이 존재하지않는 경우
        receiver = self.user_service.get_user_by_app_id(body.to_app_id)
        if receiver is None:
            return standard_response(
                message="receiver is not exist",
                data="",
                http_status=status.HTTP_400_BAD_REQUEST,
            )

        # 답장인경우
        if body.to_letter_id is not None:
            letter = self.letter_service.get_letter_by_id(letter_id=body.to_letter_id)
            # 답장을 보낼 letter_id가 존재하지않는경우
            if letter is None:
                return standard_response(
                    message="to_letter is not exist",
                    data="",
                    http_status=status.HTTP_400_BAD_REQUEST,
                )
            # 답장을 보낼 letter_id의 주인이랑 내가 보낼 편지의 수신자랑 다른경우
            if letter.from_user_id != receiver.id or letter.to_user_id != user.id:
                return standard_response(
                    message="to_app_id is not owner to_letter_id",
                    data="",
                    http_status=status.HTTP_400_BAD_REQUEST,
                )

            # 이미 답장이 있는경우
            reply_letter = self.letter_service.get_reply_letter(
                target_letter_id=letter.id
            )
            if reply_letter is not None:
                return standard_response(
                    message="already have reply",
                    data="",
                    http_status=status.HTTP_400_BAD_REQUEST,
                )

        letter_vo = self.letter_service.create_letter(
            to_user=receiver,
            to_letter_id=body.to_letter_id,
            from_user=user,
            is_anonymous=body.is_anonymous,
            writing_pad_id=body.writing_pad_id,
            envelope_id=body.envelope_id,
            stamp_id=body.stamp_id,
            content=body.content,
            title=body.title,
            font=body.font,
            will_arrive_at=body.will_arrive_at,
        )
        dicted_letter = letter_vo.to_dict()

        return standard_response(
            message="send letter successfully",
            data=dicted_letter,
            http_status=status.HTTP_201_CREATED,
        )
