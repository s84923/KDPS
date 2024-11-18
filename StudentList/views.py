from django.shortcuts import render, get_object_or_404, redirect
from KDPS.models import Student
from django import forms

# フォーム定義
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_name', 'student_class', 'school_year', 'email', 'parent_email', 'address']

# 生徒一覧表示
def student_list(request):
    search_query = request.GET.get('student_id', None)
    if search_query:
        students = Student.objects.filter(student_id__icontains=search_query)
    else:
        students = Student.objects.all()
    return render(request, 'StudentList/student_list.html', {'students': students})

# 生徒編集機能
def edit_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')  # 編集後に一覧ページにリダイレクト
    else:
        form = StudentForm(instance=student)
    return render(request, 'StudentList/edit_student.html', {'form': form, 'student': student})
