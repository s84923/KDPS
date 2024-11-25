from django.shortcuts import render, redirect
from KDPS.models import Test
from .forms import ExamCreationForm

def new_tests(request):
    if request.method == 'POST':
        form = ExamCreationForm(request.POST)
        if form.is_valid():
            # フォームデータを保存する処理
            form.save()  # test_idは自動的に生成される
            return redirect('test_list')  # 試験一覧画面にリダイレクト
    else:
        form = ExamCreationForm()

    return render(request, 'new_tests/new_tests.html', {'form': form})
