from django.db import models
from django.db import models
from django.contrib.auth.models import User
from students.models import StudentProfile

class VerificationLog(models.Model):
    ACTION_CHOICES = [
        ('VERIFIED', 'Approved / Verified'),
        ('REJECTED', 'Rejected'),
        ('RESET', 'Reset to Under Review'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='verification_logs')
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    remarks = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.registration_number} - {self.action} by {self.verified_by}"