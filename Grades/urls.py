from django.urls import path
from . import views

urlpatterns = [
    path('student_scores/', views.student_scores, name='student_scores'),  # 成績検索画面
    path('edit_student_scores/', views.edit_student_scores, name='edit_student_scores'),  # 成績編集画面
    path('overall_student_scores/', views.overall_student_scores, name='overall_student_scores'),
    path('export_overall_student_scores/', views.export_to_csv_overall, name='export_overall_student_scores'),
]

