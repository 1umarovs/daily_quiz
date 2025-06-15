from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.daily_questions, name='question'),
    path('get-question/<slug:slug>/', views.get_daily_question, name='get-question'),
]