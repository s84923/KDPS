from django.shortcuts import render, redirect
from .forms import ExamEditForm

def test_edit(request):
    if request.method == 'POST':
        form = ExamEditForm(request.POST)
        if form.is_valid():
            # ここで保存などの処理を行う
            return redirect('edit_exam')
    else:
        form = ExamEditForm()

    return render(request, 'test_edit/test_edit.html', {'form': form})
