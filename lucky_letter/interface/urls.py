from django.urls import path

from lucky_letter.interface.views import LetterView

urlpatterns = [path("letter/", view=LetterView.as_view(), name="letter")]
