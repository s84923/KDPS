from django.urls import path
from . import views

urlpatterns = [
    path('error_log/', views.error_log, name='error_log'),  # エラーログ画面
]