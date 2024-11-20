import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def send_otp(request):
    import logging
    logger = logging.getLogger(__name__)

    # リクエスト情報をログ出力
    logger.debug(f"リクエストメソッド: {request.method}")
    logger.debug(f"リクエストヘッダー: {request.headers}")
    logger.debug(f"リクエストボディ: {request.body}")

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                logger.error("メールアドレスが指定されていません。")
                return JsonResponse({"error": "メールアドレスが指定されていません。"}, status=400)

            otp = "123456"  # 固定値（テスト用）
            request.session['otp'] = otp

            logger.debug("認証コードを送信しました。")
            return JsonResponse({"message": "認証コードを送信しました。"})
        except Exception as e:
            logger.error(f"エラー: {e}")
            return JsonResponse({"error": "エラーが発生しました。", "details": str(e)}, status=500)

    logger.error("GETリクエストが送信されました。")
    return JsonResponse({"error": "このエンドポイントはGETリクエストをサポートしていません。"}, status=405)

@csrf_exempt
def verify_otp(request):
    if request.method == "POST":
        try:
            logger.debug(f"リクエストボディ: {request.body}")

            data = json.loads(request.body)
            user_otp = data.get('otp')
            session_otp = request.session.get('otp')

            if user_otp == session_otp:
                del request.session['otp']
                return JsonResponse({"message": "認証成功！"})

            return JsonResponse({"error": "認証コードが正しくありません。"}, status=400)
        except Exception as e:
            logger.error(f"エラー: {str(e)}")
            return JsonResponse({"error": "エラーが発生しました。", "details": str(e)}, status=500)

    return JsonResponse({"error": "無効なリクエストです。"}, status=400)
