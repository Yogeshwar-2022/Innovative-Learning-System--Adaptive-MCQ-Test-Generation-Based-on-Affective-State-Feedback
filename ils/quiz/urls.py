# quiz/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('question/', views.question_view, name='question_view'),
    path('submit_form/', views.submit_form, name='submit_form'),
]
