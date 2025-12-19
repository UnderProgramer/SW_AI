from django.urls import path

from . import views

app_name = "talk.board"

urlpatterns = [
    path('', views.BoardView.as_view()),
    path('<int:board_id>/', views.BoardWithId.as_view()),
]