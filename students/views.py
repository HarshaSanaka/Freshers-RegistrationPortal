from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from .models import StudentProfile, AcademicInformation
from .forms import PersonalInfoForm, AcademicInfoForm

# Required document count threshold for progress computation
TOTAL_REQUIRED_DOCUMENTS = 3

@login_required
@never_cache
def student_dashboard(request):
    profile, _ = StudentProfile.objects.get_or_create(
        user=request.user, 
        defaults={'registration_number': request.user.username}
    )
    academics, _ = AcademicInformation.objects.get_or_create(student=profile)
    
    # Calculate document upload progress
    uploaded_docs_count = request.user.documents.count() if hasattr(request.user, 'documents') else 0
    docs_percentage = min(int((uploaded_docs_count / TOTAL_REQUIRED_DOCUMENTS) * 100), 100)

    # Auto-advance DRAFT to UNDER_REVIEW once all sections are completed
    if (profile.status == 'DRAFT' and 
        profile.is_profile_complete and 
        academics.is_academic_complete and 
        uploaded_docs_count >= TOTAL_REQUIRED_DOCUMENTS):
        profile.status = 'UNDER_REVIEW'
        profile.save()

    context = {
        'profile': profile,
        'academics': academics,
        'uploaded_docs_count': uploaded_docs_count,
        'total_docs_count': TOTAL_REQUIRED_DOCUMENTS,
        'docs_percentage': docs_percentage,
    }
    return render(request, 'students/dashboard.html', context)


@login_required
@never_cache
def view_profile(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    return render(request, 'students/profile.html', {'profile': profile})


@login_required
@never_cache
def edit_profile(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Personal information updated successfully!')
            return redirect('view_profile')
    else:
        form = PersonalInfoForm(instance=profile)
    return render(request, 'students/edit_profile.html', {'form': form})


@login_required
@never_cache
def view_academics(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    academics, _ = AcademicInformation.objects.get_or_create(student=profile)
    return render(request, 'students/academics.html', {'academics': academics, 'profile': profile})


@login_required
@never_cache
def edit_academics(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    academics, _ = AcademicInformation.objects.get_or_create(student=profile)
    if request.method == 'POST':
        form = AcademicInfoForm(request.POST, instance=academics)
        if form.is_valid():
            form.save()
            messages.success(request, 'Academic information updated successfully!')
            return redirect('view_academics')
    else:
        form = AcademicInfoForm(instance=academics)
    return render(request, 'students/edit_academics.html', {'form': form})