from django.shortcuts import render, get_object_or_404, redirect
from KDPS.models import Student
from django import forms
from django.http import HttpResponse
from django.contrib import messages

# フォーム定義
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_name', 'school_year', 'student_class', 'parent_email', 'address']
        widgets = {
            'student_name': forms.TextInput(attrs={'placeholder': '名前'}),
            'school_year': forms.NumberInput(attrs={'placeholder': '学年'}),
            'student_class': forms.TextInput(attrs={'placeholder': 'クラス'}),
            'parent_email': forms.EmailInput(attrs={'placeholder': '保護者メールアドレス'}),
            'address': forms.TextInput(attrs={'placeholder': '住所'}),
        }

# 生徒一覧機能
def student_list(request):
    students = Student.objects.all()
    search_query = request.GET.get('student_id', '')

    if search_query:
        students = students.filter(student_id__icontains=search_query)

    return render(request, 'StudentList/student_list.html', {'students': students})

# 生徒編集機能
def edit_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, '保存されました')  # 保存後にメッセージを表示
            return redirect('student_list')  # 編集後に一覧ページにリダイレクト
    else:
        form = StudentForm(instance=student)
    return render(request, 'StudentList/edit_student.html', {'form': form, 'student': student})

# 生徒削除機能
def delete_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, '削除されました')  # 削除後にメッセージを表示
        return redirect('student_list')  # 削除後に生徒一覧ページへリダイレクト
    return HttpResponse(status=405)  # POST以外のリクエストは許可しない