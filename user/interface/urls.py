from django.urls import path

from user.interface.views.user_views import (
    MyRelationshipsView,
    RefreshTokenView,
    UserCheckDuplicateView,
    UserMeView,
    UserView,
)

urlpatterns = [
    path("user/token-refresh/", view=RefreshTokenView.as_view(), name="tokenRefresh"),
    path(
        "user/check-duplicate/",
        view=UserCheckDuplicateView.as_view(),
        name="userDuplicateCheck",
    ),
    path("user/me/", view=UserMeView.as_view(), name="userMe"),
    path("user/relationship/me/", MyRelationshipsView.as_view(), name="relation-me"),
    path("user/<int:app_id>/", view=UserView.as_view(), name="specificUser"),  # 특정 유저
    path("user/", view=UserView.as_view(), name="user"),  # 유저들, 혹은 유저
]
