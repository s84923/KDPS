from django.shortcuts import render, redirect
from .forms import StudentForm
from KDPS.models import User, Student
from django.db.models import Max

def student_register(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            # 生徒情報の保存
            student = form.save()

            # user_idを自動で割り振る
            user_id = User.objects.aggregate(Max('user_id'))['user_id__max'] + 1 if User.objects.exists() else 1

            # Userテーブルにデータを追加
            user = User(
                user_id=user_id,
                student_id=student,  # 修正: student インスタンスを設定
                password=form.cleaned_data['password'],
                authority=1,  # 学生としての権限
                role='student',  # Roleを学生に設定
            )
            user.save()  # Userデータベースに保存

            return redirect('student_register')  # 登録成功後のページへリダイレクト
    else:
        form = StudentForm()

    return render(request, 'student_register/student_register.html', {'form': form})
