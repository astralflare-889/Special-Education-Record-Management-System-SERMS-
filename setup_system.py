#!/usr/bin/env python
"""
SERMS Setup Script
This script helps set up the Special Education Record Management System
"""

import os
import django
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SERMS.settings')
django.setup()

from django.contrib.auth.models import User
from student_records.models import Teacher, Parent, Student

def create_sample_data():
    print("🏫 Setting up SERMS - Special Education Record Management System")
    print("=" * 60)
    
    # Create Admin User
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@school.edu',
            password='admin123',
            first_name='System',
            last_name='Administrator'
        )
        print("✅ Admin user created: admin/admin123")
    
    # Create Sample Teacher
    if not User.objects.filter(username='teacher1').exists():
        teacher_user = User.objects.create_user(
            username='teacher1',
            email='teacher1@school.edu',
            password='teacher123',
            first_name='Sarah',
            last_name='Johnson'
        )
        teacher = Teacher.objects.create(
            user=teacher_user,
            employee_id='T001',
            phone='555-0101'
        )
        print("✅ Teacher created: teacher1/teacher123 (Sarah Johnson)")
    
    # Create Sample Parent
    if not User.objects.filter(username='parent1').exists():
        parent_user = User.objects.create_user(
            username='parent1',
            email='parent1@email.com',
            password='parent123',
            first_name='Michael',
            last_name='Smith'
        )
        parent = Parent.objects.create(
            user=parent_user,
            phone='555-0201',
            address='123 Main St, City, State'
        )
        print("✅ Parent created: parent1/parent123 (Michael Smith)")
    
    # Create Sample Students
    teacher = Teacher.objects.get(employee_id='T001')
    parent = Parent.objects.get(user__username='parent1')
    
    if not Student.objects.filter(admission_number='STU001').exists():
        Student.objects.create(
            full_name='Emma Smith',
            admission_number='STU001',
            age=6,
            grade='1st Grade',
            parent_name='Michael Smith',
            parent_contact='555-0201',
            special_needs='Autism Spectrum Disorder - requires structured learning environment and visual supports',
            assigned_teacher=teacher,
            parent=parent
        )
        print("✅ Sample student created: Emma Smith")
    
    if not Student.objects.filter(admission_number='STU002').exists():
        Student.objects.create(
            full_name='James Wilson',
            admission_number='STU002',
            age=5,
            grade='Kindergarten',
            parent_name='Lisa Wilson',
            parent_contact='555-0202',
            special_needs='Speech and Language Delay - needs speech therapy and communication support',
            assigned_teacher=teacher
        )
        print("✅ Sample student created: James Wilson")
    
    print("\n🎉 SERMS Setup Complete!")
    print("=" * 60)
    print("🔐 Login Credentials:")
    print("   Admin:   admin/admin123")
    print("   Teacher: teacher1/teacher123")
    print("   Parent:  parent1/parent123")
    print("\n🚀 Start server: python manage.py runserver")
    print("🌐 Access at: http://127.0.0.1:8000")

if __name__ == '__main__':
    create_sample_data()