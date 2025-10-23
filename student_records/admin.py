from django.contrib import admin
from .models import Student, Teacher, CaseConference, Parent

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'phone']
    search_fields = ['user__first_name', 'user__last_name', 'employee_id']

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address']
    search_fields = ['user__first_name', 'user__last_name']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'admission_number', 'age', 'assigned_teacher', 'date_added']
    search_fields = ['full_name', 'admission_number']
    list_filter = ['assigned_teacher', 'grade']

@admin.register(CaseConference)
class CaseConferenceAdmin(admin.ModelAdmin):
    list_display = ['student', 'teacher', 'conference_date', 'parent_attended']
    list_filter = ['conference_date', 'parent_attended', 'teacher']
    search_fields = ['student__full_name']