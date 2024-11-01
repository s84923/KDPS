from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # ルートURLで index.html を表示
    path('admin.html', views.admin_page, name='admin_page'),  # /admin.html で admin.html を表示
    path('schedule/', views.schedule, name='schedule'),  # /schedule/ URLでスケジュールページを表示
    path('schedule/delete/<int:event_id>/', views.delete_schedule, name='delete_schedule'),  # イベント削除URL
    path('mark.html', views.mark, name='mark'),  # マーク画面
    path('report/', views.report, name='report'),  # レポートページのURLを追加
]
