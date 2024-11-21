from django.shortcuts import render, redirect
from KDPS.models import Test
from .forms import ExamEditForm

def test_list(request):
    if request.method == 'POST':
        form = ExamEditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('test_list')
    else:
        form = ExamEditForm()
def test_edit(request):
    if request.method == 'POST':
        form = ExamEditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('test_list')
    else:
        form = ExamEditForm()

    return render(request, 'test_edit/test_edit.html', {'form': form})
