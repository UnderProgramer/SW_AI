from django.urls import path

from . import views

app_name = "talk.board"

urlpatterns = [
    path('', views.CreateBoardView.as_view()),
    path('view', views.ViewBoard.as_view()),
    path('view/<int:board_id>', views.OnceViewBoard.as_view()),
    path('update/<int:board_id>', views.UpdateBoard.as_view()),
    path('delete/<int:board_id>', views.DeleteBoard.as_view()),
]