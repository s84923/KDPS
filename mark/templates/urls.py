# mark/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('mark/', views.mark, name='mark'),
]