from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import JsonResponse
from django.contrib import messages
from .models import Student, Test, Grades
import json
import os
import logging
from django.conf import settings
import calendar

# ログの設定
logger = logging.getLogger(__name__)

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
                logger.error(f"Error parsing month or day: {e}")
                messages.error(request, "日付や月の入力にエラーがあります。")
            return redirect('schedule')
        else:
            logger.warning("Month or Day is missing")
            messages.error(request, "月または日が入力されていません。")

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
    messages.success(request, "スケジュールを削除しました。")
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
            messages.success(request, "成績が追加されました。")
        except Exception as e:
            logger.error(f"データの保存中にエラーが発生: {e}")
            messages.error(request, f"データの保存中にエラーが発生しました: {e}")

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

def send_report_to_parents(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        try:
            student = Student.objects.get(student_id=student_id)
            grades = Grades.objects.filter(student_id=student)

            subject = f"{student.student_name}さんの成績レポート"
            message = f"{student.student_name}さんの成績:\n"
            for grade in grades:
                message += f"試験名: {grade.test_id.test_name}, 点数: {grade.score}\n"

            try:
                result = send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [student.parent_email],
                )
                if result:
                    messages.success(request, f"{student.student_name}さんの成績レポートを保護者に送信しました。")
                else:
                    messages.error(request, "メール送信に失敗しました。")
            except BadHeaderError:
                messages.error(request, "不正なヘッダーが検出されました。")
            except Exception as e:
                messages.error(request, f"メール送信中にエラーが発生しました: {e}")
        except Student.DoesNotExist:
            messages.error(request, "指定された生徒が見つかりません。")
        except Exception as e:
            messages.error(request, f"エラーが発生しました: {e}")

    return redirect("report")

def overall_report(request):
    return render(request, 'KDPS/overall_report.html')

def upload(request):
    return render(request, 'KDPS/upload.html')

def markset(request):
    return render(request, 'KDPS/markset.html')
