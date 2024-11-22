# views.py
from django.shortcuts import render
from KDPS.models import Test
from .forms import ExamCreationForm

def new_tests(request):
    form = ExamCreationForm()
    if request.method == 'POST':
        form = ExamCreationForm(request.POST)
        if form.is_valid():
            # フォームデータを保存する処理を追加
            # 保存後のリダイレクトやメッセージを表示
            return render(request, 'new_tests.html')  # 作成成功のテンプレート
    return render(request, 'new_tests/new_tests.html', {'form': form})
