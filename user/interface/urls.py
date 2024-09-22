from django.urls import path

from user.interface.views.user_views import RefreshTokenView

urlpatterns = [
    path("user/token-refresh", view=RefreshTokenView.as_view(), name="tokenRefresh")
]
