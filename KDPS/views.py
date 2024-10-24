# KDPS/views.py

from django.shortcuts import render

def index(request):
    return render(request, 'KDPS/index.html')  # 'KDPS/index.html' テンプレートをレンダリング
