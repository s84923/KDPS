from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # ルートURL
    path('admin.html', views.admin_page, name='admin_page'),  # /admin.html で admin.html を表示
]
