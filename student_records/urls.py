from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Login pages for each role
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-signup/', views.admin_signup, name='admin_signup'),
    path('teacher-login/', views.teacher_login, name='teacher_login'),
    path('parent-login/', views.parent_login, name='parent_login'),
    path('teacher-signup/', views.teacher_signup, name='teacher_signup'),
    path('parent-signup/', views.parent_signup, name='parent_signup'),
    path('logout/', views.user_logout, name='logout'),
    
    # Dashboards
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('parent/', views.parent_dashboard, name='parent_dashboard'),
    
    # Student management (Teachers)
    path('teacher/add-student/', views.add_student, name='add_student'),
    path('teacher/edit-student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('teacher/report/<int:student_id>/', views.generate_report, name='generate_report'),
    
    # Student details and conferences
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
    path('student/<int:student_id>/conference/', views.create_conference, name='create_conference'),
    
    # Admin management
    path('admin/students/', views.manage_students, name='manage_students'),
    path('admin/add-student/', views.admin_add_student, name='admin_add_student'),
    path('admin/teachers/', views.manage_teachers, name='manage_teachers'),
    path('admin/parents/', views.manage_parents, name='manage_parents'),
    path('admin/assign-teachers/', views.assign_teachers, name='assign_teachers'),
    path('admin/reports/', views.system_reports, name='system_reports'),
]