from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Student(models.Model):
    GRADE_CHOICES = [
        ('Playgroup', 'Playgroup / Pre-Nursery'),
        ('Nursery', 'Nursery'),
        ('PP1', 'Pre-Primary 1 (KG1)'),
        ('PP2', 'Pre-Primary 2 (KG2)'),
    ]
    
    full_name = models.CharField(max_length=100)
    admission_number = models.CharField(max_length=20, unique=True)
    age = models.PositiveIntegerField()
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, blank=True)
    parent_name = models.CharField(max_length=100)
    parent_contact = models.CharField(max_length=15)
    special_needs = models.TextField(blank=True, null=True)
    assigned_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.admission_number})"

class CaseConference(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    conference_date = models.DateField()
    progress_notes = models.TextField()
    goals_met = models.TextField()
    new_goals = models.TextField()
    parent_attended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.full_name} - {self.conference_date}"

