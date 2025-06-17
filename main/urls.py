from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.daily_questions, name='question'),
    path('get-question/<slug:slug>/', views.get_daily_question, name='get-question'),
    path("add-sample-questions/", views.insert_sample_questions, name="add_sample_questions"),
    # path("delete-sample-questions/", views.delete_sample_questions, name="delete_sample_questions"),
]