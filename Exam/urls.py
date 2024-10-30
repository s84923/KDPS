from django.urls import path
from . import views

urlpatterns = [
    path('exam_management/', views.exam_management, name='exam_management'),
]
