"""ils URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# ils/urls.py

from django.contrib import admin
# Import include function
from django.urls import path, include

urlpatterns = [
    # Include the URL patterns of your app
    path('admin/', admin.site.urls),
    path('quiz/', include('quiz.urls')),
    path('exam/', include('exam.urls')),
    path('question_bank/', include('question_bank.urls'))
]
