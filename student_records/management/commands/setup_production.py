from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from student_records.models import Teacher, Parent, Student

class Command(BaseCommand):
    help = 'Set up production database with sample data'

    def handle(self, *args, **options):
        # Create admin user
        if not User.objects.filter(is_superuser=True).exists():
            admin = User.objects.create_user(
                username='admin',
                password='admin123',
                first_name='System',
                last_name='Administrator',
                email='admin@serms.com',
                is_superuser=True,
                is_staff=True
            )
            self.stdout.write('Admin user created')

        # Create teacher user
        if not User.objects.filter(username='teacher1').exists():
            teacher_user = User.objects.create_user(
                username='teacher1',
                password='teacher123',
                first_name='Sarah',
                last_name='Johnson',
                email='sarah@serms.com'
            )
            Teacher.objects.create(
                user=teacher_user,
                employee_id='T001',
                phone='+1 555-0123'
            )
            self.stdout.write('Teacher user created')

        # Create parent user
        if not User.objects.filter(username='parent1').exists():
            parent_user = User.objects.create_user(
                username='parent1',
                password='parent123',
                first_name='John',
                last_name='Smith',
                email='john@example.com'
            )
            Parent.objects.create(
                user=parent_user,
                phone='+1 555-0456',
                address='123 Main St, City, State'
            )
            self.stdout.write('Parent user created')

        self.stdout.write(self.style.SUCCESS('Production setup completed'))