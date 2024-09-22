from django.urls import path

from user.interface.views.user_views import RefreshTokenView, UserRelationView

urlpatterns = [
    path("user/token-refresh", view=RefreshTokenView.as_view(), name="tokenRefresh"),
    path("user/<str:app_id>/", UserRelationView.as_view(), name="user-relation"),
]
