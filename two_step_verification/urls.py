# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('otp-verification/', views.otp_verification, name='otp_verification'),  # 2段階認証ページへのURL
]
