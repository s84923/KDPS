from django.shortcuts import render
from KDPS.models import ErrorLog

def error_log(request):
    # エラーログを取得してテンプレートに渡す
    logs = ErrorLog.objects.all().order_by('-timestamp')
    return render(request, 'error_log.html', {'logs': logs})
