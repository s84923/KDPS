from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import Student, Test, Grades
import json
import os
from django.conf import settings
import calendar

SCHEDULE_FILE = os.path.join(settings.BASE_DIR, 'KDPS', 'data', 'schedule.json')

def load_schedule():
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_schedule(schedule_data):
    with open(SCHEDULE_FILE, 'w', encoding='utf-8') as file:
        json.dump(schedule_data, file, ensure_ascii=False, indent=4)

def index(request):
    return render(request, 'KDPS/index.html')

def admin_page(request):
    return render(request, 'KDPS/admin.html')

def schedule(request):
    if request.method == 'POST':
        month = request.POST.get('month')
        day = request.POST.get('day')
        event_name = request.POST.get('event_name', '')

        if month and day:
            try:
                new_event = {
                    "id": len(load_schedule()), 
                    "month": int(month), 
                    "day": int(day), 
                    "event_name": event_name
                }
                schedule_data = load_schedule()
                schedule_data.append(new_event)
                save_schedule(schedule_data)
            except ValueError as e:
                print(f"Error parsing month or day: {e}")
            return redirect('schedule')
        else:
            print("Error: Month or Day is missing")

    selected_year = int(request.GET.get('year', 2024))
    selected_month = int(request.GET.get('month', 1))
    previous_month = selected_month - 1 if selected_month > 1 else 12
    next_month = selected_month + 1 if selected_month < 12 else 1
    previous_year = selected_year - 1 if selected_month == 1 else selected_year
    next_year = selected_year + 1 if selected_month == 12 else selected_year

    schedules = load_schedule()
    month_calendar = calendar.Calendar().monthdayscalendar(selected_year, selected_month)
    years = list(range(2024, 2031))
    months = list(range(1, 13))
    days = list(range(1, 32))

    return render(request, 'KDPS/schedule.html', {
        'schedules': schedules,
        'calendar': month_calendar,
        'months': months,
        'days': days,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'previous_month': previous_month,
        'next_month': next_month,
        'previous_year': previous_year,
        'next_year': next_year,
        'years': years,
    })

def schedule_view(request):
    selected_year = int(request.GET.get('year', 2024))
    selected_month = int(request.GET.get('month', 1))
    
    previous_month = selected_month - 1 if selected_month > 1 else 12
    next_month = selected_month + 1 if selected_month < 12 else 1
    previous_year = selected_year - 1 if selected_month == 1 else selected_year
    next_year = selected_year + 1 if selected_month == 12 else selected_year
    
    schedules = load_schedule()
    month_calendar = calendar.Calendar().monthdayscalendar(selected_year, selected_month)
    years = list(range(2024, 2031))
    months = list(range(1, 13))
    
    context = {
        'schedules': schedules,
        'calendar': month_calendar,
        'years': years,
        'months': months,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'previous_month': previous_month,
        'next_month': next_month,
        'previous_year': previous_year,
        'next_year': next_year,
    }
    return render(request, 'KDPS/scheduleview.html', context)

def delete_schedule(request, event_id):
    schedule_data = load_schedule()
    schedule_data = [event for event in schedule_data if event["id"] != event_id]
    save_schedule(schedule_data)
    return redirect('schedule')

def mark(request):
    return render(request, 'KDPS/mark.html')

def individual_report(request):
    if request.method == "POST":
        # 点数の追加
        test_id = request.POST.get("test_id")
        student_id = request.POST.get("student_id")
        score = request.POST.get("score")

        try:
            student = Student.objects.get(student_id=student_id)
            test = Test.objects.get(test_id=test_id)
            Grades.objects.create(test_id=test, student_id=student, score=score)
        except Exception as e:
            return JsonResponse({"error": f"データの保存中にエラーが発生しました: {e}"}, status=500)

        return redirect("report")

    # 試験データと成績データを取得
    students = Student.objects.all()
    tests = Test.objects.all()
    grades = Grades.objects.select_related("test_id", "student_id").all()  # 修正済み

    return render(request, "KDPS/report.html", {
        "students": students,
        "tests": tests,
        "grades": grades,
    })


# 保護者に成績レポートを送信
def send_report_to_parents(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        try:
            student = Student.objects.get(student_id=student_id)
            grades = Grades.objects.filter(student=student)

            subject = f"{student.student_name}さんの成績レポート"
            message = f"{student.student_name}さんの成績:\n"
            for grade in grades:
                message += f"試験名: {grade.test.test_name}, 点数: {grade.score}\n"

            # メール送信
            result = send_mail(
                subject,
                message,
                "noreply@example.com",  # 送信元
                [student.parent_email],  # 保護者のメールアドレス
            )
            print(f"メール送信結果: {result}")  # ログに結果を出力（成功: 1, 失敗: 0）

            return redirect("report")
        except Exception as e:
            return render(request, "KDPS/report.html", {"error": f"レポート送信中にエラーが発生しました: {e}"})

    return redirect("report")

def overall_report(request):
    return render(request, 'KDPS/overall_report.html')

def upload(request):
    return render(request, 'KDPS/upload.html')

def markset(request):
    return render(request, 'KDPS/markset.html')
