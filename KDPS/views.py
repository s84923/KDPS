from django.shortcuts import render, redirect
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

def delete_schedule(request, event_id):
    schedule_data = load_schedule()
    schedule_data = [event for event in schedule_data if event["id"] != event_id]
    save_schedule(schedule_data)
    return redirect('schedule')
def admin_page(request):
    return render(request, 'KDPS/admin.html')
def index(request):
    return render(request, 'KDPS/index.html')  # メインメニュー画面
def mark(request):
    return render(request, 'KDPS/mark.html')
