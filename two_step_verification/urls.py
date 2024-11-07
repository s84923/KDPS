# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('two_step_verification/', views.two_step_verification, name='two_step_verification'),
]
