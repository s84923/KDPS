from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from KDPS.models import Student, Grades, Test
from django.db.models import F
from django.template.loader import render_to_string  # 修正: render_to_stringをインポート
from django.core.cache import cache  # キャッシュを使用してデータを保存
import csv
import pdfkit

def student_scores(request):
    student_id = request.GET.get('student_id', '').strip()
    results = []
    error_message = None

    # 学籍番号が数字かどうかを確認
    if student_id and not student_id.isdigit():
        error_message = "学籍番号は数字で入力してください。"
    elif student_id:
        try:
            # データベースから関連情報を取得
            student = Student.objects.get(student_id=student_id)
            results = list(Grades.objects.filter(student_id=student)
                .select_related('test_id')
                .annotate(test_name=F('test_id__test_name'), teacher_id=F('test_id__teacher_id'))
                .values('test_name', 'teacher_id', 'score'))
            # 検索結果をキャッシュに保存
            cache.set('export_results', results, timeout=300)  # 5分間保持
        except Student.DoesNotExist:
            error_message = "指定された学籍番号の生徒が見つかりません。"

    # エクスポート処理
    if 'export' in request.GET:
        export_format = request.GET.get('export_format')
        # キャッシュから検索結果を取得
        cached_results = cache.get('export_results', [])
        if export_format == 'csv':
            return export_to_csv(cached_results)
        elif export_format == 'pdf':
            return export_to_pdf(cached_results)

    return render(request, 'Grades/student_scores.html', {
        'results': results,
        'student_id': student_id,
        'error_message': error_message,
    })

def export_to_csv(results):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_scores.csv"'

    writer = csv.writer(response)
    writer.writerow(['テスト名', '担当教員', '点数'])
    if results:
        for result in results:
            writer.writerow([result['test_name'], result['teacher_id'], result['score']])

    return response

def export_to_pdf(results):
    html = render_to_string('Grades/student_scores_pdf.html', {'results': results})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="student_scores.pdf"'
    response.write(pdfkit.from_string(html, False))
    return response

def edit_score(request, student_id):
    # 指定された student_id の成績データを取得
    grade = get_object_or_404(Grades, student_id=student_id)
    
    if request.method == 'POST':
        form = EditScoreForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('student_scores')  # 成績一覧画面にリダイレクト
    else:
        form = EditScoreForm(instance=grade)

    return render(request, 'Grades/edit_score.html', {'form': form})
