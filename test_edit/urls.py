# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('test_edit/', views.test_edit, name='test_edit'),
]
