from django.urls import path

from user.interface.views.user_views import (
    MyRelationshipsView,
    RefreshTokenView,
    UserCheckDuplicateView,
    UserMeView,
    UserView,
    get_received_letters,
    get_sent_letters,
    get_specific_letter,
)

urlpatterns = [
    # 인증된 user(자기자신)
    path("me/relationship/", MyRelationshipsView.as_view(), name="relation-me"),
    path("me/letter-box/sent/", get_sent_letters, name="get_sent_letters"),
    path("me/letter-box/received/", get_received_letters, name="get_received_letters"),
    path("me/letter-box/<str:letter_id>/", get_specific_letter, name="get_my_letter"),
    path("me/", view=UserMeView.as_view(), name="userMe"),
    path("user/token-refresh/", view=RefreshTokenView.as_view(), name="tokenRefresh"),
    path(
        "user/check-duplicate/",
        view=UserCheckDuplicateView.as_view(),
        name="userDuplicateCheck",
    ),
    path("user/<int:app_id>/", view=UserView.as_view(), name="specificUser"),  # 특정 유저
    path("user/", view=UserView.as_view(), name="user"),  # 유저들, 혹은 유저
]
