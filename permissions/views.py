# views.py
from django.shortcuts import render

def permission_edit(request):
    # 編集するデータをテンプレートに渡したい場合は、contextに追加します
    context = {
        # 例: "users": users
    }
    return render(request, 'permissions/permissions.html', context)
