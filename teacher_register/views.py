# views.py
from django.shortcuts import render, redirect
from .forms import TeacherForm  # 教員フォームのインポート

def teacher_register(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()  # 教員データをデータベースに保存
            return redirect('teacher_list')  # 登録後に一覧ページにリダイレクト
    else:
        form = TeacherForm()  # GETリクエスト時には空のフォームを表示
    
    # フォームをテンプレートに渡す
    return render(request, 'teacher_register/teacher_register.html', {'form': form})
