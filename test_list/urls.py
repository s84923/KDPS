from django.urls import path
from . import views

urlpatterns = [
    path('test_list/', views.test_list, name='test_list'),
    path('test_edit/<int:test_id>/', views.test_edit, name='test_edit'),  # 編集用のURL
]
