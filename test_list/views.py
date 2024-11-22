from django.shortcuts import render, redirect, get_object_or_404
from KDPS.models import Test
from .forms import ExamEditForm

# 試験一覧ビュー
def test_list(request):
    tests = Test.objects.all()  # すべての試験を取得
    if request.method == 'POST':
        form = ExamEditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('test_list')
    else:
        form = ExamEditForm()

    # テンプレートに試験一覧とフォームを渡す
    return render(request, 'test_list.html', {'form': form, 'tests': tests})

# 試験編集ビュー
def test_edit(request, test_id):
    instance = get_object_or_404(Test, id=test_id)  # 該当の試験データを取得
    if request.method == 'POST':
        form = ExamEditForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('test_list')
    else:
        form = ExamEditForm(instance=instance)

    return render(request, 'test_edit/test_edit.html', {'form': form})
