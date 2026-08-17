from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    STATUS_CHOICES = [
        ('DRAFT', 'Incomplete Application'),
        ('UNDER_REVIEW', 'Under Review'),
        ('VERIFIED', 'Verified / Approved'),
        ('REJECTED', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    registration_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_profile_complete(self):
        return bool(self.date_of_birth and self.gender and self.phone and self.address)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.registration_number})"


class AcademicInformation(models.Model):
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science and Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('MECH', 'Mechanical Engineering'),
        ('CIVIL', 'Civil Engineering'),
        ('IT', 'Information Technology'),
    ]

    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name='academics')
    
    # 10th Schooling
    tenth_school = models.CharField(max_length=150, blank=True)
    tenth_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    tenth_passing_year = models.PositiveIntegerField(null=True, blank=True)

    # 12th / Diploma
    intermediate_college = models.CharField(max_length=150, blank=True)
    intermediate_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    intermediate_passing_year = models.PositiveIntegerField(null=True, blank=True)

    # College Program
    course = models.CharField(max_length=50, default="B.Tech")
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES, blank=True)
    admission_year = models.PositiveIntegerField(default=2026)

    @property
    def is_academic_complete(self):
        return bool(
            self.tenth_school and self.tenth_percentage and self.tenth_passing_year and
            self.intermediate_college and self.intermediate_percentage and self.branch
        )

    def __str__(self):
        return f"Academics - {self.student.registration_number}"