from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from letter import settings
from letter.views import HealthChecker
from lucky_letter.interface import urls as letter_urls
from user.interface import urls as user_urls

schema_view = get_schema_view(
    openapi.Info(
        title="Letter API",
        default_version="v1",
        description="API documentation for the Letter project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r"^$", view=HealthChecker.as_view(), name="HealthChecker"),
    re_path(r"^", include(user_urls)),
    re_path(r"^", include(letter_urls)),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
