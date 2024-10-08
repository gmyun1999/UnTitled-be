from rest_framework import status
from rest_framework.decorators import api_view

from common.interface.http_response import standard_response
from user.domain.user_role import UserRole
from user.domain.user_token import UserTokenPayload, UserTokenType
from user.infra.token.user_token_manager import UserTokenManager
from user.interface.validator.user_token_validator import validate_token
from user.service.user_service import UserLetterBoxService


@api_view(["GET"])
@validate_token(
    roles=[UserRole.USER], validate_type=UserTokenType.ACCESS, view_type="function"
)
def get_specific_letter(
    request,
    letter_id: str,
    token_payload: UserTokenPayload,
):
    user_letter_box_service = UserLetterBoxService()
    user_token_manager = UserTokenManager()
    current_user = user_token_manager.get_current_user(user_payload_vo=token_payload)
    letter = user_letter_box_service.fetch_letter(
        letter_id=letter_id, user_id=current_user.id
    )

    if letter is None:
        return standard_response(
            message="no letter",
            data="",
            http_status=status.HTTP_200_OK,
        )

    return standard_response(
        message="fetch letter", data=letter, http_status=status.HTTP_200_OK
    )


@api_view(["GET"])
@validate_token(
    roles=[UserRole.USER], validate_type=UserTokenType.ACCESS, view_type="function"
)
def get_received_letters(
    request,
    token_payload: UserTokenPayload,
):
    user_letter_box_service = UserLetterBoxService()
    user_token_manager = UserTokenManager()
    current_user = user_token_manager.get_current_user(user_payload_vo=token_payload)
    letters_data = user_letter_box_service.fetch_received_letter(
        user_id=current_user.id
    )

    if letters_data is None:
        return standard_response(
            message="letter box is empty",
            data=letters_data,
            http_status=status.HTTP_200_OK,
        )
    return standard_response(
        message="fetch received letters",
        data=letters_data,
        http_status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@validate_token(
    roles=[UserRole.USER], validate_type=UserTokenType.ACCESS, view_type="function"
)
def get_sent_letters(
    request,
    token_payload: UserTokenPayload,
):
    user_letter_box_service = UserLetterBoxService()
    user_token_manager = UserTokenManager()
    current_user = user_token_manager.get_current_user(user_payload_vo=token_payload)
    letters_data = user_letter_box_service.fetch_sended_letter(user_id=current_user.id)

    if letters_data is None:
        return standard_response(
            message="letter box is empty",
            data=letters_data,
            http_status=status.HTTP_200_OK,
        )
    return standard_response(
        message="fetch received letters",
        data=letters_data,
        http_status=status.HTTP_200_OK,
    )
