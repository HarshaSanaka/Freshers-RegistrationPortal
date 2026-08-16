from django.db import models
import os
from django.db import models
from django.contrib.auth.models import User

def student_upload_path(instance, filename):
    # Files are saved to media/documents/<admission_number>/<doc_type>/<filename>
    admission_no = instance.user.student_profile.admission_number if hasattr(instance.user, 'student_profile') else instance.user.username
    return os.path.join('documents', str(admission_no), instance.document_type, filename)

class StudentDocument(models.Model):
    DOCUMENT_TYPES = [
        ('10TH_MARKSHEET', '10th Standard Marksheet'),
        ('12TH_MARKSHEET', '12th Standard Marksheet'),
        ('GOVT_ID', 'Government ID Proof (Aadhaar/Passport/PAN)'),
        ('TC', 'Transfer Certificate (TC)'),
        ('PHOTO', 'Passport Size Photo'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending Verification'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to=student_upload_path)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    rejection_reason = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Prevent duplicate uploads of the same document type for a single student
        unique_together = ('user', 'document_type')

    def __str__(self):
        return f"{self.user.username} - {self.get_document_type_display()}"