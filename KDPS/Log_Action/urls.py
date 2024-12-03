from django.urls import path
from . import views

urlpatterns = [
    path('action_log/', views.action_log, name='action_log'),
    path('action_log/export/', views.export_logs, name='export_logs'),
]