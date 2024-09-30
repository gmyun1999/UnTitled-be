from typing import Any, Optional

from rest_framework.response import Response


def standard_response(
    message: str, data: Optional[Any] = None, http_status: int = 200
) -> Response:
    return Response({"message": message, "data": data}, status=http_status)
