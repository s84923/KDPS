from django.urls import path
from . import views

urlpatterns = [
    path('test_list/', views.test_list, name='test_list'),
    path('test/edit/<int:test_id>/', views.test_edit, name='test_edit'),  # 編集用のURL
    path('new_tests/', views.new_tests, name='new_tests'),
]


