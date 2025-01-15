from django.shortcuts import render, redirect, get_object_or_404
from KDPS.models import Test
from .forms import ExamEditForm
from .forms import ExamCreationForm
from django.contrib import messages
from django.http import HttpResponse

# 保存後にメッセージを表示
def test_list(request):
    tests = Test.objects.all()
    if request.method == 'POST':
        form = ExamEditForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '試験が更新されました。')  # メッセージを送信
            return redirect('test_list')
    else:
        form = ExamEditForm()

    return render(request, 'test_list.html', {'form': form, 'tests': tests})

# 新規作成後にメッセージを表示
def new_tests(request):
    if request.method == 'POST':
        form = ExamCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '新しい試験が作成されました。')  # メッセージを送信
            return redirect('test_list')
    else:
        form = ExamCreationForm()

    return render(request, 'new_tests.html', {'form': form})

# 試験編集ビュー
def test_edit(request, test_id):
    # 試験データを取得
    instance = get_object_or_404(Test, test_id=test_id)

    if request.method == 'POST':
        if 'delete' in request.POST:  # 削除処理
            instance.delete()
            messages.success(request, '試験が削除されました。')
            return redirect('test_list')  # 削除後に試験一覧にリダイレクト
        else:  # 編集処理
            form = ExamEditForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, '試験が更新されました。')  # メッセージを送信
                return redirect('test_list')  # 編集後に試験一覧にリダイレクト
    else:
        form = ExamEditForm(instance=instance, initial={'test_id': instance.test_id})

    return render(request, 'test_list/test_edit.html', {'form': form})