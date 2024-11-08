# StudentList/views.py

from django.shortcuts import render
from KDPS.models import Student  # KDPSアプリ内のStudentモデルをインポート

def student_list(request):
    class_name = request.GET.get('class_name')
    student_id = request.GET.get('student_id')
    
    # 生徒データを取得し、検索フィルタを適用
    students = Student.objects.all()
    if class_name:
        students = students.filter(student_class=class_name)
    if student_id:
        students = students.filter(student_id=student_id)
    
    return render(request, 'StudentList/student_list.html', {'students': students})

def edit_student(request, student_id):
    # 編集ページへのプレースホルダー関数（生徒編集ページを将来的に実装）
    return render(request, 'StudentList/edit_student.html', {'student_id': student_id})
