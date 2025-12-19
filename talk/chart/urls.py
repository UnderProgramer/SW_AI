from django.urls import path

from . import views

app_name = "talk.chart"

urlpatterns = [
    path('', views.ChartView.as_view()),
]