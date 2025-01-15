from django.shortcuts import render, redirect
from .forms import TeacherForm
from KDPS.models import Teacher, User
from django.db.models import Max
from django.contrib import messages  # messagesをインポート

# 教員登録処理
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

            # メッセージをトースト通知用に保存
            messages.success(request, '教員が登録されました。')

            # 登録後に教員登録画面にリダイレクト
            return redirect('teacher_register')  # ここを変更
    else:
        form = TeacherForm()  # GETリクエスト時には空のフォームを表示

    return render(request, 'teacher_register/teacher_register.html', {'form': form})
