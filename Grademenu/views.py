from django.shortcuts import render

def Grademenu(request):
    return render(request, 'Grademenu/Grademenu.html')  # テンプレートのパスを変更
