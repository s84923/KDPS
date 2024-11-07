from django.urls import path
from . import views

urlpatterns = [
    path('student_register/', views.student_register, name='student_register'),
]
