from statistics import median
from django.shortcuts import render
from KDPS.models import Student, Grades
from django.db.models import F, Max

def student_grades_view(request):
    # セッションからログイン中の生徒情報を取得
    student_id = request.session.get('user_id')
    results = []

    if student_id:
        try:
            # ログイン中の生徒情報を取得
            student = Student.objects.get(student_id=student_id)

            # 成績情報を取得
            results = list(
                Grades.objects.filter(student_id=student)
                .select_related('test_id')
                .annotate(
                    test_name=F('test_id__test_name'),
                    teacher_id=F('test_id__teacher_id'),
                )
                .values('test_name','teacher_id', 'score', 'test_id')
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

                # 結果に統計情報を追加
                result['max_score'] = max_score
                result['median_score'] = median_score
                result['participant_count'] = participant_count

        except Student.DoesNotExist:
            pass  # 生徒が存在しない場合は何もしない

    return render(request, 'StudentGrades/student_grades.html', {
        'results': results,
    })
