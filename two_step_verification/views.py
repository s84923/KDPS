# views.py
from django.shortcuts import render

def otp_verification(request):
    return render(request, 'otp_verification.html')  # 'otp_verification.html'はテンプレート名
