# views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from KDPS.models import ActionLog
import csv

def action_log(request):
    logs = ActionLog.objects.filter(user_id=request.user.id).order_by('-timestamp')
    paginator = Paginator(logs, 10)  # 1ページあたり10件表示
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # フィルタリング（例: 日付やアクション）
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    action_filter = request.GET.get('action')

    if start_date and end_date:
        logs = logs.filter(timestamp__range=[start_date, end_date])
    if action_filter:
        logs = logs.filter(action__icontains=action_filter)

    return render(request, 'action_log.html', {'page_obj': page_obj, 'logs': logs})

def export_logs(request):
    # レスポンスのコンテンツタイプを設定
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="action_logs.csv"'

    # CSVライターを初期化
    writer = csv.writer(response)

    # ヘッダー行を書き込む
    writer.writerow(['ログID', 'ユーザーID', 'アクション', 'タイムスタンプ'])

    # データベースからすべてのログを取得し、CSVに書き込む
    logs = ActionLog.objects.all()
    for log in logs:
        writer.writerow([log.log_id, log.user_id, log.action, log.timestamp])

    return response