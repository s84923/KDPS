from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # メインメニュー
    path('admin.html', views.admin_page, name='admin_page'),  # /admin.html で admin.html を表示
    path('schedule/', views.schedule, name='schedule'),  # スケジュールページ
    path('schedule/delete/<int:event_id>/', views.delete_schedule, name='delete_schedule'),  # イベント削除URL
    path('mark.html', views.mark, name='mark'),  # 採点画面
    path('report/', views.individual_report, name='report'),  # 個人成績レポートを'report'として定義
    path('overall_report/', views.overall_report, name='overall_report'),  # 全体成績レポート
]
