from django.urls import path

from lucky_letter.interface.views import LetterView, ReplyLetterView

urlpatterns = [
    path(
        "letter/<str:letter_id>/reply", view=ReplyLetterView.as_view(), name="letter_me"
    ),  # 특정 편지id로 답장한 letter
    path(
        "letter/<str:letter_id>", view=LetterView.as_view(), name="letter_me"
    ),  # 특정 편지id
    path("letter/", view=LetterView.as_view(), name="letter"),  # 편지 생성
]
