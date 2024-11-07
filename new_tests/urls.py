# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('new_tests/', views.new_tests, name='new_tests'),
]
