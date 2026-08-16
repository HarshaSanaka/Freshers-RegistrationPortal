from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending Verification'),
        ('VERIFIED', 'Verified / Approved'),
        ('REJECTED', 'Rejected'),
    ]

    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science & Engineering'),
        ('ECE', 'Electronics & Communication'),
        ('MECH', 'Mechanical Engineering'),
        ('CIVIL', 'Civil Engineering'),
        ('IT', 'Information Technology'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    admission_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField()

    # Academic Information
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES)
    tenth_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="10th Grade Score")
    twelfth_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="12th Grade Score")

    # Document Uploads
    marksheet_10th = models.FileField(upload_to='documents/10th/')
    marksheet_12th = models.FileField(upload_to='documents/12th/')
    id_proof = models.FileField(upload_to='documents/id_proofs/')

    # Admin Control
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    admin_remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.admission_number})"
