from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),  # ログインページへのURL
    path('login/', views.login_view, name='login'),  # ログインページ
]
