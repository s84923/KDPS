from django.urls import path
from . import views

urlpatterns = [
    path('student_grades/', views.student_grades_view, name='student_grades'),
]
