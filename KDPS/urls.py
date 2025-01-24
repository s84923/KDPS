from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),  # メインメニュー
    path('admin.html', views.admin_page, name='admin_page'),  # 管理者画面
    path('schedule_view/', views.schedule_view, name='schedule_view'),  # 閲覧専用スケジュール
    path('schedule/', views.schedule, name='schedule'),  # スケジュール設定（編集用）
    path('schedule/delete/<int:event_id>/', views.delete_schedule, name='delete_schedule'),  # イベント削除
    path('report/', views.individual_report, name='report'),  # 個人成績レポート
    path('send_report/', views.send_report_to_parents, name='send_report'),  # 保護者に成績レポートと評価文送信
    path('overall_report/', views.overall_report, name='overall_report'),  # 全体成績レポート
    path('upload/', views.upload, name='upload'),  # ファイルアップロード
    path('markset.html', views.markset, name='markset'),  # 採点設定画面
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
]