from django.urls import path

from . import views

app_name = "talk.comment"

urlpatterns = [
    path('comment', views.BoardCommentView.as_view()),
]