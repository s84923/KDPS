from statistics import median
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from KDPS.models import Student, Grades, Test
from django.db.models import F, Max, Count, Avg
from django.template.loader import render_to_string
from django.core.cache import cache
from weasyprint import HTML
import csv
import pandas as pd
from django.contrib import messages

def student_scores(request):
    student_id = request.GET.get('student_id', '').strip()
    results = []
    error_message = None
    student_name = None  # 生徒名を初期化

    if student_id and not student_id.isdigit():
        error_message = "学籍番号は数字で入力してください。"
    elif student_id:
        try:
            # 生徒情報の取得
            student = Student.objects.get(student_id=student_id)
            student_name = student.student_name  # 生徒名を取得

            # テスト結果の詳細を取得
            results = list(
                Grades.objects.filter(student_id=student)
                .select_related('test_id')
                .annotate(
                    test_name=F('test_id__test_name'),
                    teacher_id=F('test_id__teacher_id'),
                )
                .values('test_name', 'teacher_id', 'score', 'test_id')
            )

            # 各テストの統計情報を追加
            for result in results:
                test_id = result['test_id']

                # 最高点
                max_score = (
                    Grades.objects.filter(test_id=test_id)
                    .aggregate(Max('score'))['score__max']
                )

                # 中央値
                scores = list(
                    Grades.objects.filter(test_id=test_id).values_list('score', flat=True)
                )
                median_score = median(scores) if scores else None

                # 受験人数
                participant_count = len(scores)

                # 結果に追加
                result['max_score'] = max_score
                result['median_score'] = median_score
                result['participant_count'] = participant_count

            # キャッシュに保存
            cache.set('export_results', {'results': results, 'student_name': student_name}, timeout=300)

        except Student.DoesNotExist:
            error_message = "指定された学籍番号の生徒が見つかりません。"

    # エクスポート処理
    if 'export' in request.GET:
        export_format = request.GET.get('export_format')
        cached_data = cache.get('export_results', {'results': [], 'student_name': None})
        cached_results = cached_data['results']
        cached_student_name = cached_data['student_name']
        if export_format == 'csv':
            return export_to_csv(cached_results)
        elif export_format == 'pdf':
            return export_to_pdf(cached_results, cached_student_name)

    return render(request, 'Grades/student_scores.html', {
        'results': results,
        'student_id': student_id,
        'error_message': error_message,
        'student_name': student_name,
    })


def export_to_csv(results):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_scores.csv"'

    writer = csv.writer(response)
    writer.writerow(['テスト名', '担当教員', '点数', '最高点', '中央値', '受験人数'])
    if results:
        for result in results:
            writer.writerow([ 
                result['test_name'],
                result['teacher_id'],
                result['score'],
                result.get('max_score', ''),
                result.get('median_score', ''),
                result.get('participant_count', '')
            ])

    return response


def export_to_pdf(results, student_name):
    html = render_to_string('Grades/student_scores_pdf.html', {
        'results': results,
        'student_name': student_name,  # 生徒名をテンプレートに渡す
    })
    pdf = HTML(string=html).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="student_scores.pdf"'
    return response


def edit_student_scores(request):
    student_id = request.GET.get('student_id', '').strip()
    results = []
    error_message = None
    student_name = None

    if student_id and student_id.isdigit():
        try:
            # 学生情報を取得
            student = Student.objects.get(student_id=student_id)
            student_name = student.student_name  # 生徒名を取得
            # 成績を取得
            results = list(Grades.objects.filter(student_id=student)
                           .select_related('test_id')  # test_id を含む関連情報を取得
                           .annotate(test_name=F('test_id__test_name'), teacher_id=F('test_id__teacher_id'))
                           .values('test_name', 'teacher_id', 'score', 'test_id', 'id'))  # test_id と id を取得

            # 各テストの統計情報を計算
            for result in results:
                test_id = result['test_id']

                # 最高点
                max_score = (
                    Grades.objects.filter(test_id=test_id)
                    .aggregate(Max('score'))['score__max']
                )

                # 中央値
                scores = list(
                    Grades.objects.filter(test_id=test_id).values_list('score', flat=True)
                )
                median_score = median(scores) if scores else None

                # 受験人数
                participant_count = len(scores)

                # 結果に追加
                result['max_score'] = max_score
                result['median_score'] = median_score
                result['participant_count'] = participant_count

            # POSTリクエストの場合、得点を更新または削除
            if request.method == 'POST':
                grade_id = request.POST.get('grade_id')  # hiddenフィールドからgrade_idを取得
                new_score = request.POST.get('new_score')  # 新しい得点
                if 'update' in request.POST and grade_id and new_score is not None:
                    try:
                        grade = Grades.objects.get(id=grade_id)
                        grade.score = new_score  # 新しい得点に更新
                        grade.save()  # 保存
                        messages.success(request, '更新されました!')  # 成功メッセージを表示
                    except Grades.DoesNotExist:
                        error_message = "指定された成績が見つかりません。"
                elif 'delete' in request.POST and grade_id:
                    try:
                        grade = Grades.objects.get(id=grade_id)
                        grade.delete()  # 成績を削除
                        messages.success(request, '削除されました!')  # 成功メッセージを表示
                    except Grades.DoesNotExist:
                        error_message = "指定された成績が見つかりません。"

                # 更新または削除後、再度GETリクエストとしてリダイレクトして最新のデータを表示
                return redirect(f'/edit_student_scores/?student_id={student_id}')  # リダイレクト

        except Student.DoesNotExist:
            error_message = "指定された学籍番号の生徒が見つかりません。"

    return render(request, 'Grades/edit_student_scores.html', {
        'results': results,
        'student_id': student_id,
        'student_name': student_name,  # 生徒名をテンプレートに渡す
        'error_message': error_message,
    })

def overall_student_scores(request):
    results = []
    student_class = request.GET.get('student_class', '')
    school_year = request.GET.get('school_year', '')
    export_format = request.GET.get('export_format', '')

    if student_class and school_year:
        # 学年とクラスで絞り込む
        results = (
            Grades.objects.filter(student_id__student_class=student_class, student_id__school_year=school_year)
            .select_related('test_id')  # test_id に関連する情報を取得
            .values('test_id__test_name', 'test_id__teacher_id', 'test_id')  # test_id も含める
            .annotate(
                max_score=Max('score'),
                participant_count=Count('score')
            )
        )

        # 各テストの中央値を計算
        for result in results:
            test_id = result['test_id']

            # 絞り込んだ学年とクラスの結果のみ取得
            scores = list(Grades.objects.filter(test_id=test_id, student_id__student_class=student_class, student_id__school_year=school_year).values_list('score', flat=True))

            if scores:
                result['median_score'] = median(scores)  # 中央値を計算
            else:
                result['median_score'] = None  # スコアがない場合は中央値なし

        # キャッシュにデータを保存（5分間保持）
        cache.set('overall_student_scores_data', results, timeout=300)

    if export_format == 'csv':
        return export_to_csv_overall(request)
    elif export_format == 'pdf':
        return export_to_pdf_overall(request)
    
    return render(request, 'Grades/overall_student_scores.html', {'results': results, 'student_class': student_class, 'school_year': school_year})


def export_to_csv_overall(request):
    # GETパラメータを取得
    student_class = request.GET.get('student_class', '')
    school_year = request.GET.get('school_year', '')

    # 空文字の場合、クエリパラメータを使わない
    filter_conditions = {}
    if student_class:
        filter_conditions['student_id__student_class'] = student_class
    if school_year:
        filter_conditions['student_id__school_year'] = school_year

    # 学年とクラスで絞り込んだデータを取得
    results = (
        Grades.objects.filter(**filter_conditions)
        .select_related('test_id')  # test_id に関連する情報を取得
        .values('test_id__test_name', 'test_id__teacher_id', 'test_id')  # test_id も含める
        .annotate(
            max_score=Max('score'),
            participant_count=Count('score')
        )
    )

    # 各テストの中央値を計算
    for result in results:
        test_id = result['test_id']  # ここで正しく 'test_id' を参照できるように修正

        # 対象テストのスコアを絞り込んだ学年とクラスの結果のみ取得
        scores = list(Grades.objects.filter(test_id=test_id, **filter_conditions).values_list('score', flat=True))
        if scores:
            result['median_score'] = median(scores)  # 中央値を計算

    # CSVとしてエクスポート
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="overall_student_scores.csv"'

    writer = csv.writer(response)
    writer.writerow(['テスト名', '担当教員', '最高点', '中央値', '受験人数'])

    for result in results:
        writer.writerow([
            result['test_id__test_name'],
            result['test_id__teacher_id'],
            result['max_score'],
            result.get('median_score', ''),
            result['participant_count'],
        ])

    return response

# def export_to_pdf_overall(request):
#     # GETパラメータを取得
#     student_class = request.GET.get('student_class', '')
#     school_year = request.GET.get('school_year', '')

#     # 空文字の場合、クエリパラメータを使わない
#     filter_conditions = {}
#     if student_class:
#         filter_conditions['student_id__student_class'] = student_class
#     if school_year:
#         filter_conditions['student_id__school_year'] = school_year

#     # 学年とクラスで絞り込んだデータを取得
#     results = (
#         Grades.objects.filter(**filter_conditions)
#         .select_related('test_id')  # test_id に関連する情報を取得
#         .values('test_id__test_name', 'test_id__teacher_id', 'test_id')  # test_id も含める
#         .annotate(
#             max_score=Max('score'),
#             participant_count=Count('score')
#         )
#     )

#     # 各テストの中央値を計算
#     for result in results:
#         test_id = result['test_id']  # ここで正しく 'test_id' を参照できるように修正

#         # 対象テストのスコアを絞り込んだ学年とクラスの結果のみ取得
#         scores = list(Grades.objects.filter(test_id=test_id, **filter_conditions).values_list('score', flat=True))
#         if scores:
#             result['median_score'] = median(scores)  # 中央値を計算

#     # PDFとしてエクスポート
#     html = render_to_string('Grades/overall_student_scores_pdf.html', {'results': results})
#     pdf = HTML(string=html).write_pdf()

#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="overall_student_scores.pdf"'

#     return response

def export_to_pdf_overall(request):
    # GETパラメータを取得
    student_class = request.GET.get('student_class', '')
    school_year = request.GET.get('school_year', '')

    # 空文字の場合、クエリパラメータを使わない
    filter_conditions = {}
    if student_class:
        filter_conditions['student_id__student_class'] = student_class
    if school_year:
        filter_conditions['student_id__school_year'] = school_year

    # 学年とクラスで絞り込んだデータを取得
    results = (
        Grades.objects.filter(**filter_conditions)
        .select_related('test_id')  # test_id に関連する情報を取得
        .values('test_id__test_name', 'test_id__teacher_id', 'test_id')  # test_id も含める
        .annotate(
            max_score=Max('score'),
            participant_count=Count('score')
        )
    )

    # 各テストの中央値を計算
    for result in results:
        test_id = result['test_id']  # ここで正しく 'test_id' を参照できるように修正

        # 対象テストのスコアを絞り込んだ学年とクラスの結果のみ取得
        scores = list(Grades.objects.filter(test_id=test_id, **filter_conditions).values_list('score', flat=True))
        if scores:
            result['median_score'] = median(scores)  # 中央値を計算

    # PDFとしてエクスポート
    html = render_to_string('Grades/overall_student_scores_pdf.html', {
        'results': results,
        'student_class': student_class,  # 学年
        'school_year': school_year,  # クラス
    })
    pdf = HTML(string=html).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="overall_student_scores.pdf"'

    return response
