# views.py
from django.shortcuts import render

def two_step_verification(request):
    return render(request, 'two_step_verification/two_step_verification.html')  # 'two_step_verification.html'はテンプレート名
