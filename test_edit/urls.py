# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('test_list/', views.test_list, name='test_list'),
    path('/test/test_edit/<int:student_id>/', views.test_edit, name='test_edit'),
]
