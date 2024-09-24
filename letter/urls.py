from django.conf.urls import include
from django.urls import re_path

from letter.views import HealthChecker
from lucky_letter.interface import urls as letter_urls
from user.interface import urls as user_urls

urlpatterns = [
    re_path(r"^$", view=HealthChecker.as_view(), name="HealthChecker"),
    re_path(r"^", include(user_urls)),
    re_path(r"^", include(letter_urls)),
]
