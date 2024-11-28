from django.urls import path
from . import views

urlpatterns = [
    path('teacher_register/', views.teacher_register, name='teacher_register'),
]


