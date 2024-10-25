from django.shortcuts import render

def index(request):
    return render(request, 'KDPS/index.html')  # 既存の index.html

def admin_page(request):
    return render(request, 'KDPS/admin.html')  # admin.html をレンダリング

