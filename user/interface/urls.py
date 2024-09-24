from django.urls import path

from user.interface.views.user_views import MyRelationshipsView, RefreshTokenView

urlpatterns = [
    path("user/token-refresh", view=RefreshTokenView.as_view(), name="tokenRefresh"),
    path("user/me/", MyRelationshipsView.as_view(), name="relation-me"),
]
