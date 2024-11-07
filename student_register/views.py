from django.shortcuts import render

def student_register(request):
    return render(request, 'student_register/student_register.html')  # テンプレートのパスを変更
