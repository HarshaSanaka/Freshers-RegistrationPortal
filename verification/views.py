from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from students.models import StudentProfile
from documents.models import StudentDocument
from .models import VerificationLog

def is_staff_user(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_staff_user)
def verification_dashboard(request):
    """List all students categorized by their registration status."""
    status_filter = request.GET.get('status', 'ALL')
    
    if status_filter != 'ALL':
        students = StudentProfile.objects.filter(status=status_filter).select_related('user', 'academics')
    else:
        students = StudentProfile.objects.all().select_related('user', 'academics')
        
    counts = {
        'all': StudentProfile.objects.count(),
        'under_review': StudentProfile.objects.filter(status='UNDER_REVIEW').count(),
        'verified': StudentProfile.objects.filter(status='VERIFIED').count(),
        'rejected': StudentProfile.objects.filter(status='REJECTED').count(),
        'draft': StudentProfile.objects.filter(status='DRAFT').count(),
    }

    return render(request, 'verification/verification_list.html', {
        'students': students,
        'counts': counts,
        'active_filter': status_filter
    })

@user_passes_test(is_staff_user)
def student_verification_detail(request, pk):
    """Comprehensive single-page inspection for an applicant."""
    student = get_object_or_404(StudentProfile.objects.select_related('user', 'academics'), pk=pk)
    documents = StudentDocument.objects.filter(user=student.user)
    logs = student.verification_logs.order_by('-timestamp')

    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks', '').strip()

        if action in ['VERIFIED', 'REJECTED', 'UNDER_REVIEW']:
            student.status = action
            student.save()

            # Record audit trail
            VerificationLog.objects.create(
                student=student,
                verified_by=request.user,
                action=action,
                remarks=remarks
            )
            messages.success(request, f"Student {student.registration_number} status updated to {student.get_status_display()}.")
            return redirect('student_verification_detail', pk=student.pk)

    return render(request, 'verification/student_detail.html', {
        'student': student,
        'documents': documents,
        'logs': logs,
    })

@login_required
def admission_slip(request, pk):
    """Printable confirmation slip for verified students."""
    student = get_object_or_404(StudentProfile.objects.select_related('user', 'academics'), pk=pk)
    
    # Students can only view their own slip; staff can view any
    if not request.user.is_staff and student.user != request.user:
        return HttpResponseForbidden("Unauthorized access.")
        
    if student.status != 'VERIFIED':
        messages.error(request, "Admission slip is only available after application verification.")
        return redirect('student_dashboard')

    return render(request, 'verification/admission_slip.html', {'student': student})