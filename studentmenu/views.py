from django.shortcuts import render

def studentmenu(request):
    return render(request, 'studentmenu/studentmenu.html')  # テンプレートのパスを変更
