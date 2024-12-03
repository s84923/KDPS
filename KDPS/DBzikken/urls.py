from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_user, name='add_user'),     # ユーザー登録ページ
    
    path('user_list/', views.user_list, name='user_list'),
    # 他の URL パターン

]

