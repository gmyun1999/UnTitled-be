from rest_framework.exceptions import APIException, status


class UnprocessableEntity(APIException):
    def __init__(
        self,
        detail="Unprocessable Entity",
    ):
        super().__init__(detail, None)

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class NotFound(APIException):
    def __init__(
        self,
        detail="Not Found",
    ):
        super().__init__(detail, None)

    status_code = status.HTTP_404_NOT_FOUND


class Unauthorized(APIException):
    def __init__(
        self,
        detail="Unauthorized",
    ):
        super().__init__(detail, None)

    status_code = status.HTTP_401_UNAUTHORIZED


class UserNotFound(APIException):
    def __init__(
        self,
        detail="user Not Found",
    ):
        super().__init__(detail, None)

    status_code = status.HTTP_404_NOT_FOUND
