from django.urls import path

from user.interface.views.user_auth_views import (
    RefreshTokenView,
    save_push_service_token,
)
from user.interface.views.user_letter_box_views import (
    get_received_letters,
    get_sent_letters,
    get_specific_letter,
)
from user.interface.views.user_notification_views import (
    UserNotificationSettingView,
    UserNotificationView,
)
from user.interface.views.user_relation_views import MyRelationshipsView
from user.interface.views.user_views import UserCheckDuplicateView, UserMeView, UserView

urlpatterns = [
    # 인증된 user(자기자신)
    path("me/relationship/", MyRelationshipsView.as_view(), name="relation-me"),
    path("me/letter-box/sent/", get_sent_letters, name="get_sent_letters"),
    path("me/letter-box/received/", get_received_letters, name="get_received_letters"),
    path("me/letter-box/<str:letter_id>/", get_specific_letter, name="get_my_letter"),
    path(
        "me/notification/setting",
        view=UserNotificationSettingView.as_view(),
        name="user_notification_setting",
    ),
    path(
        "me/notification/",
        view=UserNotificationView.as_view(),
        name="user_notification",
    ),
    path("me/", view=UserMeView.as_view(), name="userMe"),
    path("user/token-refresh/", view=RefreshTokenView.as_view(), name="tokenRefresh"),
    path(
        "user/check-duplicate/",
        view=UserCheckDuplicateView.as_view(),
        name="userDuplicateCheck",
    ),
    path("user/push-token/", save_push_service_token, name="save_push_service_token"),
    path("user/", view=UserView.as_view(), name="user"),  # 유저들, 혹은 유저
]
