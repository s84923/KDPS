from django.contrib import admin
from .models import Student, Grades, User, Teacher, Test, ErrorLog, ActionLog, AuthTokens, Profile

# 生徒情報
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'student_name', 'school_year', 'student_class', 'email', 'parent_email', 'address')
    search_fields = ('student_name', 'student_id', 'school_year', 'student_class')
    list_filter = ('school_year', 'student_class')

# 成績情報
@admin.register(Grades)
class GradesAdmin(admin.ModelAdmin):
    list_display = ('test_id', 'student_id', 'score')
    search_fields = ('test_id', 'student_id__student_name')
    list_filter = ('test_id',)

# ユーザー情報
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'student_id', 'teacher_id', 'authority')
    search_fields = ('user_id', 'student_id__student_name', 'teacher_id')
    list_filter = ('authority',)

# 教員情報
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'teacher_name', 'school_year', 'student_class', 'post')
    search_fields = ('teacher_name', 'teacher_id')
    list_filter = ('school_year', 'student_class', 'post')

# 試験情報
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('test_id', 'test_name', 'teacher_id')
    search_fields = ('test_name', 'teacher_id')
    list_filter = ('teacher_id',)

# エラーログ
@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ('error_id', 'user_id', 'error_message', 'timestamp')
    search_fields = ('user_id', 'error_message')
    list_filter = ('timestamp',)

# アクションログ
@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('log_id', 'user_id', 'action', 'timestamp')
    search_fields = ('user_id', 'action')
    list_filter = ('timestamp',)

# 2段階認証
@admin.register(AuthTokens)
class AuthTokensAdmin(admin.ModelAdmin):
    list_display = ('token_id', 'user_id', 'created_at', 'expires_at')
    search_fields = ('user_id', 'token')
    list_filter = ('created_at', 'expires_at')

# ユーザープロフィール
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'grade', 'class_name')
    search_fields = ('user__user_id', 'student_id')
    list_filter = ('grade', 'class_name')
