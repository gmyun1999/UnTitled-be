from django.conf.urls import include
from django.urls import path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from letter import settings
from letter.views import HealthChecker
from lucky_letter.interface import urls as letter_urls
from user.interface import urls as user_urls

urlpatterns = [
    re_path(r"^$", view=HealthChecker.as_view(), name="HealthChecker"),
    re_path(r"^", include(user_urls)),
    re_path(r"^", include(letter_urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
