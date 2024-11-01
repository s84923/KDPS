from django.urls import path
from . import views

urlpatterns = [
    path('student_scores/', views.student_scores, name='student_scores'),  # 成績検索画面
    path('edit_score/<int:student_id>/', views.edit_score, name='edit_score'),  # 成績編集画面
]
