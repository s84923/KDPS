from django.shortcuts import render, get_object_or_404, redirect
from KDPS.models import Teacher
from django import forms
from django.http import HttpResponse
from django.contrib import messages

# フォーム定義
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher_name', 'school_year','student_class', 'post', 'email']
        widgets = {
            'teacher_name': forms.TextInput(attrs={'placeholder': '名前'}),
            'school_year': forms.NumberInput(attrs={'placeholder': '担当学年'}),
            'student_class': forms.TextInput(attrs={'placeholder': '担当クラス'}),
            'post': forms.TextInput(attrs={'placeholder': '役職'}),
            'email': forms.EmailInput(attrs={'placeholder': 'メールアドレス'}),
        }

# 生徒一覧機能
def teacher_list(request):
    # Teacherの情報を取得（userのroleが'teacher'のデータ）
    teachers = Teacher.objects.all()

    # teachersをテンプレートに渡して表示
    return render(request, 'TeacherList/teacher_list.html', {'teachers': teachers})
# 生徒編集機能
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, '保存されました')  # 保存後にメッセージを表示
            return redirect('teacher_list')  # 編集後に一覧ページにリダイレクト
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'TeacherList/edit_teacher.html', {'form': form, 'teacher': teacher})

# 生徒削除機能
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, '削除されました')  # 削除後にメッセージを表示
        return redirect('teacher_list')  # 削除後に生徒一覧ページへリダイレクト
    return HttpResponse(status=405)  # POST以外のリクエストは許可しない