from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import StudentSearchForm  # フォームを後ほど作成
import csv
import pdfkit  # PDFエクスポートのために、別途インストールが必要です（例: pip install pdfkit）

def student_scores(request):
    form = StudentSearchForm(request.GET or None)
    results = []

    if form.is_valid() and 'search' in request.GET:
        student_name = form.cleaned_data['student_name']
        # DBが完成したら以下のようにフィルタリングに置き換える
        # results = StudentScore.objects.filter(student__name__icontains=student_name)
        # 仮のデータを設定
        results = [{'test_name': 'テスト1', 'score': 80}, {'test_name': 'テスト2', 'score': 90}]

    # エクスポート処理
    if 'export' in request.GET:
        export_format = request.GET.get('export_format')
        if export_format == 'csv':
            return export_to_csv(results)
        elif export_format == 'pdf':
            return export_to_pdf(results)

    return render(request, 'Grades/student_scores.html', {'form': form, 'results': results})

def export_to_csv(results):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_scores.csv"'

    writer = csv.writer(response)
    writer.writerow(['Test Name', 'Score'])
    for result in results:
        writer.writerow([result['test_name'], result['score']])

    return response

def export_to_pdf(results):
    html = render_to_string('Grades/student_scores_pdf.html', {'results': results})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="student_scores.pdf"'
    response.write(pdfkit.from_string(html, False))
    return response

def edit_score(request, student_id):
    # 成績編集画面への遷移（後で実装）
    return HttpResponse(f"編集画面（ID: {student_id}）")
