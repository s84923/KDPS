from django.shortcuts import render

def teacher_register(request):
    return render(request, 'teacher_register/teacher_register.html')  # テンプレートのパスを変更
