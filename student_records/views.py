from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from .models import Student, Teacher, CaseConference, Parent
from django.contrib.auth.models import User

def is_admin(user):
    return user.is_superuser

def is_teacher(user):
    return hasattr(user, 'teacher')

def is_parent(user):
    return hasattr(user, 'parent')

def home(request):
    return render(request, 'student_records/home.html')

# Separate login views for each role
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        messages.error(request, 'Invalid admin credentials')
    return render(request, 'student_records/admin_login.html')

def teacher_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and hasattr(user, 'teacher'):
            login(request, user)
            return redirect('teacher_dashboard')
        messages.error(request, 'Invalid teacher credentials')
    return render(request, 'student_records/teacher_login.html')

def parent_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and hasattr(user, 'parent'):
            login(request, user)
            return redirect('parent_dashboard')
        messages.error(request, 'Invalid parent credentials')
    return render(request, 'student_records/parent_login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

# Teacher Signup
def teacher_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        employee_id = request.POST['employee_id']
        phone = request.POST['country_code'] + ' ' + request.POST['phone']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'student_records/teacher_signup.html')
        
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        
        Teacher.objects.create(
            user=user,
            employee_id=employee_id,
            phone=phone
        )
        
        messages.success(request, 'Teacher account created successfully! Please login.')
        return redirect('teacher_login')
    
    return render(request, 'student_records/teacher_signup.html')

# Parent Signup
def parent_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['country_code'] + ' ' + request.POST['phone']
        address = request.POST['address']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'student_records/parent_signup.html')
        
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        
        Parent.objects.create(
            user=user,
            phone=phone,
            address=address
        )
        
        messages.success(request, 'Parent account created successfully! Please login.')
        return redirect('parent_login')
    
    return render(request, 'student_records/parent_signup.html')

# Admin Signup (Limited to 2 admins)
def admin_signup(request):
    # Check if there are already 2 admins
    admin_count = User.objects.filter(is_superuser=True).count()
    if admin_count >= 2:
        messages.error(request, 'Maximum 2 administrators allowed. Contact existing admin for access.')
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        admin_code = request.POST['admin_code']
        
        # Simple admin verification code
        if admin_code != 'SERMS2024ADMIN':
            messages.error(request, 'Invalid administrator verification code')
            return render(request, 'student_records/admin_signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'student_records/admin_signup.html')
        
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_superuser=True,
            is_staff=True
        )
        
        messages.success(request, 'Administrator account created successfully! Please login.')
        return redirect('admin_login')
    
    return render(request, 'student_records/admin_signup.html')

# Admin Dashboard - Controls everything
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_parents = Parent.objects.count()
    total_conferences = CaseConference.objects.count()
    total_admins = User.objects.filter(is_superuser=True).count()
    
    recent_students = Student.objects.order_by('-date_added')[:5]
    recent_conferences = CaseConference.objects.order_by('-created_at')[:5]
    
    return render(request, 'student_records/admin_dashboard.html', {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_parents': total_parents,
        'total_conferences': total_conferences,
        'total_admins': total_admins,
        'recent_students': recent_students,
        'recent_conferences': recent_conferences,
    })

# Teacher Dashboard - Add students, fill forms, create reports
@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    teacher = request.user.teacher
    students = Student.objects.filter(assigned_teacher=teacher).order_by('admission_number')
    recent_conferences = CaseConference.objects.filter(teacher=teacher).order_by('-created_at')[:5]
    
    return render(request, 'student_records/teacher_dashboard.html', {
        'students': students,
        'recent_conferences': recent_conferences
    })

# Parent Dashboard - Search and view their children
@login_required
@user_passes_test(is_parent)
def parent_dashboard(request):
    parent = request.user.parent
    students = Student.objects.filter(parent=parent).order_by('admission_number')
    
    # Search functionality for parents
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(
            Q(full_name__icontains=search_query) | 
            Q(admission_number__icontains=search_query)
        ).order_by('admission_number')
    
    recent_conferences = CaseConference.objects.filter(student__parent=parent).order_by('-created_at')[:5]
    
    return render(request, 'student_records/parent_dashboard.html', {
        'students': students,
        'recent_conferences': recent_conferences,
        'search_query': search_query
    })

# Student management for teachers
@login_required
@user_passes_test(is_teacher)
def add_student(request):
    if request.method == 'POST':
        teacher = request.user.teacher
        special_needs_text = request.POST.get('special_needs_description', '') if request.POST.get('has_special_needs') == 'yes' else 'No special needs'
        
        student = Student.objects.create(
            full_name=request.POST['full_name'],
            admission_number=request.POST['admission_number'],
            age=request.POST['age'],
            grade=request.POST['grade'],
            parent_name=request.POST['parent_name'],
            parent_contact=request.POST['country_code'] + ' ' + request.POST['parent_contact'],
            special_needs=special_needs_text,
            assigned_teacher=teacher
        )
        messages.success(request, f'Student {student.full_name} added successfully!')
        return redirect('teacher_dashboard')
    return render(request, 'student_records/add_student.html')

@login_required
@user_passes_test(is_teacher)
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    teacher = request.user.teacher
    
    if student.assigned_teacher != teacher:
        messages.error(request, 'You can only edit your assigned students')
        return redirect('teacher_dashboard')
    
    if request.method == 'POST':
        student.full_name = request.POST['full_name']
        student.age = request.POST['age']
        student.grade = request.POST['grade']
        student.parent_name = request.POST['parent_name']
        student.parent_contact = request.POST['parent_contact']
        student.special_needs = request.POST.get('special_needs_description', '') if request.POST.get('has_special_needs') == 'yes' else 'No special needs'
        student.save()
        messages.success(request, f'Student {student.full_name} updated successfully!')
        return redirect('student_detail', student_id=student.id)
    
    return render(request, 'student_records/edit_student.html', {'student': student})

# Student details with role-based access
@login_required
def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    # Check permissions
    if request.user.is_superuser:
        pass  # Admin can see all
    elif hasattr(request.user, 'teacher'):
        if student.assigned_teacher != request.user.teacher:
            messages.error(request, 'Access denied')
            return redirect('teacher_dashboard')
    elif hasattr(request.user, 'parent'):
        if student.parent != request.user.parent:
            messages.error(request, 'Access denied')
            return redirect('parent_dashboard')
    else:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    conferences = CaseConference.objects.filter(student=student).order_by('-conference_date')
    return render(request, 'student_records/student_detail.html', {
        'student': student, 
        'conferences': conferences
    })

# Case conference creation for teachers
@login_required
@user_passes_test(is_teacher)
def create_conference(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    teacher = request.user.teacher
    
    if student.assigned_teacher != teacher:
        messages.error(request, 'You can only create conferences for your assigned students')
        return redirect('teacher_dashboard')
    
    if request.method == 'POST':
        conference = CaseConference.objects.create(
            student=student,
            teacher=teacher,
            conference_date=request.POST['conference_date'],
            progress_notes=request.POST['progress_notes'],
            goals_met=request.POST['goals_met'],
            new_goals=request.POST['new_goals'],
            parent_attended=request.POST.get('parent_attended') == 'on'
        )
        messages.success(request, 'Case conference created successfully!')
        return redirect('student_detail', student_id=student.id)
    return render(request, 'student_records/create_conference.html', {'student': student})

# Report generation for teachers
@login_required
@user_passes_test(is_teacher)
def generate_report(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    teacher = request.user.teacher
    
    if student.assigned_teacher != teacher:
        messages.error(request, 'Access denied')
        return redirect('teacher_dashboard')
    
    conferences = CaseConference.objects.filter(student=student).order_by('-conference_date')
    
    return render(request, 'student_records/student_report.html', {
        'student': student,
        'conferences': conferences,
        'teacher': teacher
    })

# Admin views for managing everything
@login_required
@user_passes_test(is_admin)
def manage_students(request):
    students = Student.objects.all().order_by('admission_number')
    return render(request, 'student_records/manage_students.html', {'students': students})

@login_required
@user_passes_test(is_admin)
def admin_add_student(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('assigned_teacher')
        teacher = Teacher.objects.get(id=teacher_id) if teacher_id else None
        special_needs_text = request.POST.get('special_needs_description', '') if request.POST.get('has_special_needs') == 'yes' else 'No special needs'
        
        student = Student.objects.create(
            full_name=request.POST['full_name'],
            admission_number=request.POST['admission_number'],
            age=request.POST['age'],
            grade=request.POST['grade'],
            parent_name=request.POST['parent_name'],
            parent_contact=request.POST['country_code'] + ' ' + request.POST['parent_contact'],
            special_needs=special_needs_text,
            assigned_teacher=teacher
        )
        messages.success(request, f'Student {student.full_name} added successfully!')
        return redirect('manage_students')
    
    teachers = Teacher.objects.all()
    return render(request, 'student_records/admin_add_student.html', {'teachers': teachers})

@login_required
@user_passes_test(is_admin)
def manage_teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'student_records/manage_teachers.html', {'teachers': teachers})

@login_required
@user_passes_test(is_admin)
def manage_parents(request):
    parents = Parent.objects.all()
    return render(request, 'student_records/manage_parents.html', {'parents': parents})

@login_required
@user_passes_test(is_admin)
def assign_teachers(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        teacher_id = request.POST.get('teacher_id')
        
        student = Student.objects.get(id=student_id)
        teacher = Teacher.objects.get(id=teacher_id) if teacher_id else None
        
        student.assigned_teacher = teacher
        student.save()
        
        if teacher:
            messages.success(request, f'{student.full_name} assigned to {teacher.user.first_name} {teacher.user.last_name}')
        else:
            messages.success(request, f'{student.full_name} unassigned from teacher')
        
        return redirect('assign_teachers')
    
    students = Student.objects.all().order_by('admission_number')
    teachers = Teacher.objects.all()
    return render(request, 'student_records/assign_teachers.html', {
        'students': students,
        'teachers': teachers
    })

@login_required
@user_passes_test(is_admin)
def system_reports(request):
    # System statistics
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_conferences = CaseConference.objects.count()
    
    # Students with special needs
    special_needs_count = Student.objects.exclude(special_needs='No special needs').count()
    
    # Unassigned students
    unassigned_students = Student.objects.filter(assigned_teacher=None).count()
    
    # Teacher workload
    teacher_workload = []
    for teacher in Teacher.objects.all():
        student_count = Student.objects.filter(assigned_teacher=teacher).count()
        teacher_workload.append({
            'teacher': teacher,
            'student_count': student_count,
            'workload_status': 'High' if student_count > 15 else 'Normal' if student_count > 5 else 'Low'
        })
    
    return render(request, 'student_records/system_reports.html', {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_conferences': total_conferences,
        'special_needs_count': special_needs_count,
        'unassigned_students': unassigned_students,
        'teacher_workload': teacher_workload,
    })