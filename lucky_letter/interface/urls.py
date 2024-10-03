from django.urls import path

from lucky_letter.interface.views import LettersView, LetterView

urlpatterns = [
    path(
        "letter/<int:letter_id>", view=LetterView.as_view(), name="letter_me"
    ),  # 특정 편지id
    path("letter/", view=LetterView.as_view(), name="letter"),  # 편지 생성
    path("letters/", view=LettersView.as_view(), name="letter_me"),  # 편지 여러개
]
