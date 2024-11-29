# views.py
from django.shortcuts import render, redirect
from .forms import TeacherForm
from KDPS.models import Teacher, User
from django.db.models import Max

def teacher_register(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save()  # Teacherデータベースに保存

            # ユーザーIDの自動生成 (次のIDを取得)
            user_id = User.objects.aggregate(Max('user_id'))['user_id__max'] + 1 if User.objects.exists() else 1

            # Userテーブルにデータを追加
            user = User(
                user_id=user_id,
                teacher_id=teacher.teacher_id,  # teacher_idをUserに追加
                password=form.cleaned_data['password'],
                authority=2,  # Teacherとしての権限
                role='teacher',  # Roleを教師に設定
            )
            user.save()  # Userデータベースに保存

            # 登録後に一覧ページにリダイレクト
            # return redirect('teacher_list')

    else:
        form = TeacherForm()  # GETリクエスト時には空のフォームを表示

    return render(request, 'teacher_register/teacher_register.html', {'form': form})
