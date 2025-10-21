from django.urls import path

from . import views

app_name = "talk.comment"

urlpatterns = [
    path('', views.BoardCommentView.as_view()),
    path('<int:id>', views.BoardCommentOnceView.as_view()),
]