from django.shortcuts import render, redirect
from .forms import StudentForm
from KDPS.models import Student, User
from django.db.models import Max

def student_register(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()

            user_id = User.objects.aggregate(Max('user_id'))['user_id__max'] + 1 if User.objects.exists() else 1

          # Userテーブルにデータを追加
            user = User(
                user_id=user_id,
                teacher_id=student.student_id,  # teacher_idをUserに追加
                password=form.cleaned_data['password'],
                authority=1,  # Teacherとしての権限
                role='student',  # Roleを教師に設定
            )
            user.save()  # Userデータベースに保存


            return redirect('student_register')  # 登録成功後のページへリダイレクト
    else:
        form = StudentForm()

    return render(request, 'student_register/student_register.html', {'form': form})