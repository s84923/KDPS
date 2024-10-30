from django.shortcuts import render

def exam_management(request):
    return render(request, 'Exam/exam_management.html')  # テンプレートのパスを変更
