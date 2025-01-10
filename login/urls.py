from django.urls import path,include
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('studentmenu/', include('studentmenu.urls')),  # 生徒用メニュー
    path('techermenu/', include('KDPS.urls')),  
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
