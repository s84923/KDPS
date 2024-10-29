from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),         # Django 管理画面
    path('', include('KDPS.urls')),          # KDPS アプリの URL をインクルード
    path('accounts/', include('django.contrib.auth.urls')),  # Django 認証URLをインクルード
]
