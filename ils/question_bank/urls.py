# question_bank/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.run_model, name='run_model'),
]
