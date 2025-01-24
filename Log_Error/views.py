from django.shortcuts import render
from KDPS.models import ErrorLog
from django.http import JsonResponse

def error_log(request):
    try:
        # エラーログを取得してテンプレートに渡す
        logs = ErrorLog.objects.all().order_by('-timestamp')
        return render(request, 'error_log.html', {'logs': logs})
    except Exception as e:
        # エラーが発生した場合はログに記録し、適切なレスポンスを返す
        print(f"エラー: {e}")
        return JsonResponse({'error': str(e)}, status=500)
