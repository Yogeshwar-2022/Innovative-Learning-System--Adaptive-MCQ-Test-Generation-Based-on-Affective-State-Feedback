# exam/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.exam_landing_page, name='exam_landing_page'),
    path('exam_submit_form/', views.exam_submit_form, name='exam_submit_form'),
]
