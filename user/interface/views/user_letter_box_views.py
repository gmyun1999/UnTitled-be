from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from pydantic import BaseModel, Field
from rest_framework import status
from rest_framework.decorators import api_view

from common.interface.http_response import standard_response
from common.interface.validators import validate_query_params
from common.paging import Paginator
from user.domain.user_role import UserRole
from user.domain.user_token import UserTokenPayload, UserTokenType
from user.infra.models.swagger.user_letter import LetterBoxResponseSerializer
from user.infra.token.user_token_manager import UserTokenManager
from user.interface.validator.user_token_validator import validate_token
from user.service.user_letter_box_service import UserLetterBoxService


@extend_schema(
    summary=" 내 메일함의 특정 편지 가져오기",
    description="path param으로 letter_box의 id를 넘긴다",
    responses={200: LetterBoxResponseSerializer},
)
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


class PageParams(BaseModel):
    page: int | None = Field(default=None, ge=1)
    page_size: int | None = Field(default=None, ge=1)


@api_view(["GET"])
@validate_token(
    roles=[UserRole.USER], validate_type=UserTokenType.ACCESS, view_type="function"
)
@validate_query_params(PageParams, view_type="function")
def get_received_letters(
    request,
    token_payload: UserTokenPayload,
    params: PageParams,
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

    if params.page is None or params.page_size is None:  # pragma: no cover
        return standard_response(
            message="fetch received letters",
            data=letters_data,
            http_status=status.HTTP_200_OK,
        )

    paged_result = Paginator.paginate(
        items=letters_data, page=params.page, page_size=params.page_size
    )

    response_data = {
        "items": paged_result.items,
        "total_items": paged_result.total_items,
        "total_pages": paged_result.total_pages,
        "current_page": paged_result.current_page,
        "page_size": paged_result.page_size,
        "has_previous": paged_result.has_previous,
        "has_next": paged_result.has_next,
    }
    return standard_response(
        message="fetch received letters",
        data=response_data,
        http_status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@validate_token(
    roles=[UserRole.USER], validate_type=UserTokenType.ACCESS, view_type="function"
)
@validate_query_params(PageParams, view_type="function")
def get_sent_letters(
    request,
    token_payload: UserTokenPayload,
    params: PageParams,
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
    if params.page is None or params.page_size is None:
        return standard_response(
            message="fetch sent letters",
            data=letters_data,
            http_status=status.HTTP_200_OK,
        )

    paged_result = Paginator.paginate(
        items=letters_data, page=params.page, page_size=params.page_size
    )

    response_data = {
        "items": paged_result.items,
        "total_items": paged_result.total_items,
        "total_pages": paged_result.total_pages,
        "current_page": paged_result.current_page,
        "page_size": paged_result.page_size,
        "has_previous": paged_result.has_previous,
        "has_next": paged_result.has_next,
    }

    return standard_response(
        message="fetch sent letters",
        data=response_data,
        http_status=status.HTTP_200_OK,
    )
